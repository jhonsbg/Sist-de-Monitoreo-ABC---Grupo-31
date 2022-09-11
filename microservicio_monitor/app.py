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
        
        mensaje_respuesta = ""
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S") 
        filename = 'historico_sensor_monitoreo.csv'

        try: 
            content = requests.get('http://127.0.0.1:5001/sensor')        
            
            sensor = content.json()
            respuesta_string = str(sensor["Estado"])
            args = (sensor,)
            with open(filename, 'a', newline="") as file:
                file.write(dt_string)
                file.write(",") 
                file.write(respuesta_string)
                file.write("\n")
            if respuesta_string == False:
                mensaje_respuesta = 'Sensor fuera de servicio'
            elif respuesta_string == True:
                mensaje_respuesta = 'Sensor operando correctamente'
            else:
                mensaje_respuesta = 'Sistema no disponible'            
            return json.dumps(mensaje_respuesta)    
        # except requests.exceptions.sensornodisponible as errh : 
        #     with open(filename, 'a', newline="") as file:
        #         file.write(dt_string)
        #         file.write(",") 
        #         file.write("False")
        #         file.write("\n")
        #     return("Componente sensor no disponible")
        except requests.exceptions.HTTPError as errh:
            print ("Http Error: ",errh)
            with open(filename, 'a', newline="") as file:
                file.write(dt_string)
                file.write(",") 
                file.write("False")
                file.write("\n")
            return("Falla en la comunicación con componente Sensor")
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting: ",errc)
            with open(filename, 'a', newline="") as file:
                file.write(dt_string)
                file.write(",") 
                file.write("False")
                file.write("\n")
            return("Falla en la comunicación con componente Sensor")
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error: ",errt)
            with open(filename, 'a', newline="") as file:
                file.write(dt_string)
                file.write(",") 
                file.write("False")
                file.write("\n")
            return("Falla en la comunicación con componente Sensor")
        except requests.exceptions.RequestException as err:
            print ("Algo salio mal: ",err)
            with open(filename, 'a', newline="") as file:
                file.write(dt_string)
                file.write(",") 
                file.write("False")
                file.write("\n")
            return("Falla en la comunicación con componente Sensor")
    
api.add_resource(Monitor, '/monitoreo')