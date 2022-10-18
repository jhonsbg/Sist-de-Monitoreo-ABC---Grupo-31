from cgi import FieldStorage
from fileinput import filename
from microservicios_3 import create_app
from flask_restful import Resource, Api
from flask import Flask,request, send_file
import json
import random
from datetime import datetime
from .modelos import db,Upload


from flask_sqlalchemy import SQLAlchemy
from io import BytesIO


app = create_app('default')
app_context = app.app_context()
app_context.push()
api = Api(app)
api.init_app(app)

##para agregar BD 
db.init_app(app)
db.create_all()

### fin BD

class Prueba(Resource):

     def get(self):              
        respuesta =random.choice([True, False]) 
        respuesta_string = str(respuesta)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")       
        filename = 'historico_sensor.csv'
        with open(filename, 'a', newline="") as file:              
            file.write(dt_string)
            file.write(",") 
            file.write(respuesta_string) 
            file.write("\n")
        return {'Estado': respuesta}

     def post(self):
        
        myother = request.files["file"]
        print("El typo de archivo es {}".format(myother))
        print(type(myother))
        nombre = myother.filename
        print("El titulo del archivo es {}".format(nombre))
        content = request.files['file'].read()                  
        myother.save(nombre,buffer_size=16384)
        mydate = datetime.utcnow()
        mystate = "uploaded"
        ## Guardar la info en BD
        upload = Upload(filename=nombre,data = content,state=mystate,date=mydate)
        db.session.add(upload)
        db.session.commit()
        ##
        return {"mensaje": "cargue archivo {} exitoso".format(nombre)}   


class Descarga(Resource):

   def get(self,filename):
        descarga = Upload.query.filter_by(filename=filename).first()
        print(type(descarga))        
        archivo =  send_file(BytesIO(descarga.data),download_name=filename,as_attachment=True)
        print(type(archivo))               
        return archivo


api.add_resource(Prueba, '/audios')
api.add_resource(Descarga, '/audios/<string:filename>')