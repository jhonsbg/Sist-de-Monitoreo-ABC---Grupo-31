from microservicio_sensor import create_app
from flask_restful import Resource, Api
from flask import Flask
import json
import random
from datetime import datetime


app = create_app('default')
app_context = app.app_context()
app_context.push()
api = Api(app)
api.init_app(app)

class Sensor(Resource):

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

    
api.add_resource(Sensor, '/sensor')