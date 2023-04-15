from marshmallow import fields
from xml.etree.ElementInclude import include
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class UserMail(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(254))
    app = db.Column(db.String(36))
    motivo = db.Column(db.String(255))
    ip = db.Column(db.String(255))
    createdAt = db.Column(db.String(20))

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))

class UserMailSchema (SQLAlchemyAutoSchema):
    class Meta:
        model = UserMail
        include_relationships = False
        load_instance = True