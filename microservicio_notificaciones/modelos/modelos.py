from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import enum


db = SQLAlchemy()

class TipoRol(enum.Enum):
    PROPIETARIO = 1
    OPERADOR = 2
    ADMINISTRADOR = 3

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))
    estado = db.Column(db.Boolean, default=False)
    tipo_rol = db.Column(db.Enum(TipoRol))

class Geopunto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    longitud = db.Column(db.String(128))
    latitud = db.Column(db.String(128))
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    fecha = db.Column(db.String)


class NotificacionBotonPanico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notificado = db.Column(db.Boolean, default=True)
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    geopunto = db.Column(db.Integer, db.ForeignKey("geopunto.id"))
    fecha = db.Column(db.String)

class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, *kwargs):
        if value is None:
            return None
        return {'llave': value.name, 'valor': value.value}


class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True

    usuario = fields.String()
    contrasena = fields.String()
    estado = fields.Boolean()
    tipo_rol = EnumADiccionario(attribute=('tipo_rol'))


class GeopuntoSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = Geopunto
        include_relationships = True
        load_instance = True

    longitud = fields.String()
    latitud = fields.String()
    usuario = fields.String()
    fecha = fields.String()

class NotificacionBotonPanicoSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = NotificacionBotonPanico
        include_relationships = True
        load_instance = True

    notificado = fields.Boolean()
    geopunto = fields.Nested(GeopuntoSchema())
    usuario = fields.String()
    fecha = fields.String()