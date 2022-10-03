from microservicio_autentificador import create_app
from flask_restful import Resource, Api
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from .modelos.modelos import db, Usuario, UsuarioSchema, NotificacionBotonPanico
from .modelos.modelos import Geopunto, GeopuntoSchema, NotificacionBotonPanicoSchema
from flask_jwt_extended import (jwt_required, create_access_token, get_current_user, verify_jwt_in_request
)
from flask_jwt_extended import JWTManager
import requests
import json

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()
api = Api(app)

class VistaSignIn(Resource):

    def post(self):
        nuevo_usuario = Usuario(
                usuario=request.json["usuario"], tipo_rol=request.json["tipo_rol"], estado=True, contrasena=request.json["contrasena"])

        db.session.add(nuevo_usuario)
        db.session.commit()
        token_de_acceso = create_access_token(identity=nuevo_usuario.id)
        return {"mensaje": "usuario creado exitosamente", "token": token_de_acceso, "id": nuevo_usuario.id}

    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204

class VistaLogin(Resource):

    
    def post(self):
        usuario = Usuario.query.filter(Usuario.usuario == request.json["usuario"],
                                       Usuario.contrasena == request.json["contrasena"]).first()
        db.session.commit()
        if usuario is None:
            return "El usuario no existe", 404
        else:
            token_de_acceso = create_access_token(identity=usuario.id)
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso}

api.add_resource(VistaSignIn, '/signin')
api.add_resource(VistaLogin, '/login')

jwt = JWTManager(app)