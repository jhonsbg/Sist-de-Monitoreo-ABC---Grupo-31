from microservicio_seguridad import create_app
from flask_restful import Resource, Api
from flask import Flask, request
import json
import requests
import random
from datetime import datetime
from flask_jwt_extended import JWTManager, get_jwt
from flask_jwt_extended import jwt_required, create_access_token
from .modelos import db, Usuario


app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()
api = Api(app)
api.init_app(app)
jwt = JWTManager(app)

class Login(Resource):          

    def post(self):
        usuario = Usuario.query.filter(Usuario.usuario == request.json["usuario"],
                                       Usuario.contrasena == request.json["contrasena"]).first()
        db.session.commit()
        if usuario is None:
            return "El usuario no existe", 404
        else:
            token_de_acceso = create_access_token(identity=usuario.id, additional_claims = {"rol": usuario.tipoUsuario,"idUsuario": usuario.id})
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso}

api.add_resource(Login, '/login')