from microservicios_3 import create_app
from flask_restful import Api
from .modelos import db
from .vistas import Prueba,Descarga, Descarga2, Descarga3
from flask_sqlalchemy import SQLAlchemy

app = create_app('default')
app_context = app.app_context()
app_context.push()
api = Api(app)
api.init_app(app)

db.init_app(app)
db.create_all()

api.add_resource(Prueba, '/api/tasks')
api.add_resource(Descarga, '/api/files/<string:filename>')
api.add_resource(Descarga2, '/api/<string:filename>')
api.add_resource(Descarga3, '/api/example')
