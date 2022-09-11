from microservicio_monitor import create_app
from flask_restful import Resource, Api
from flask import Flask, request
import json
import requests
import random
from datetime import datetime


app = create_app('default')
app_context = app.app_context()
app_context.push()
api = Api(app)
api.init_app(app)

class Monitor(Resource):

    def post(self):
        content = requests.get('http://127.0.0.1:5001/sensor')        
        
        if content.status_code == 404:
            return content.json(),404
        else:
            sensor = content.json()
            sensor["Estado"] = request.json["Estado"]
            respuesta_string = str(sensor["Estado"])
            args = (sensor,)
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S") 
            filename = 'historico_sensor_monitoreo.csv'
            with open(filename, 'a', newline="") as file:
               file.write(dt_string)
               file.write(",") 
               file.write(respuesta_string)
               file.write("\n")
            mensaje_respuesta = ""
            if respuesta_string == False:
                mensaje_respuesta = 'Sensor fuera de servicio'
            elif respuesta_string == True:
                mensaje_respuesta = 'Sensor operando correctamente'
            else:
                mensaje_respuesta = 'Sistema no disponible'            
            return json.dumps(mensaje_respuesta)    

    
api.add_resource(Monitor, '/monitoreo')