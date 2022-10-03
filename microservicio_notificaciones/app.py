from microservicio_notificaciones import create_app
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


notbotonpanicoschema = NotificacionBotonPanicoSchema()

class VistaNotificacionBotonPanico(Resource):

    @jwt_required()
    def post(self):
        nuevo_geopunto = Geopunto(longitud=request.json["longitud"],
                                latitud=request.json["latitud"],
                                usuario=request.json["id_usuario"], 
                                fecha=request.json["fecha"])
        db.session.add(nuevo_geopunto)
        db.session.commit()
        nueva_notificacion = NotificacionBotonPanico(notificado=False,
                                geopunto=nuevo_geopunto.id,
                                usuario=request.json["id_usuario"], 
                                fecha=request.json["fecha"])
        db.session.add(nueva_notificacion)
        db.session.commit()
        return notbotonpanicoschema.dump(nueva_notificacion)

    @jwt_required()
    def get(self):
        return [notbotonpanicoschema.dump(notificacion) for notificacion in NotificacionBotonPanico.query.filter(NotificacionBotonPanico.usuario == request.json["id_usuario"]).all()]


api.add_resource(VistaNotificacionBotonPanico, '/boton-panico')
jwt = JWTManager(app)