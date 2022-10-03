from microservicio_seguridad import create_app
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

class Login(Resource):

    def get(self):           
        
        respuesta_string = "Alarma Activa 1"        
        return {'dashboard': respuesta_string}   


api.add_resource(Login, '/login')