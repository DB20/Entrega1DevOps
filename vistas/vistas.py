from tokenize import String
from flask import request, jsonify
from flask_jwt_extended import jwt_required, create_access_token,get_jwt
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
import decimal
import json
from flask.json import JSONEncoder
from flask import current_app as app



from modelo import db, User, UserMail, UserMailSchema

UserMailSchema = UserMailSchema()


class VistaSignIn(Resource):

    def post(self):
        try:
            username = request.json["username"]
            password = request.json["password"]
        except:
            return {"Message": "Diligencie todos los campos de la solicitud"}, 400

        user = User.query.filter_by(username = username).all()
        if user:
            return {"Message": "El usuario o el correo ya está registrado"}, 412
        else:
            # fechaactual= datetime.now()
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            id_user = User.query.filter_by(username = username).first()
            return {"id": id_user.id}, 201

class VistaLogIn(Resource):

    def post(self):
        try:
            username = request.json["username"]
            password = request.json["password"]
        except:
            return {"Message": "Diligencie todos los campos de la solicitud"}, 400
        usuario = User.query.filter(User.username == username,
                                    User.password == password).first()
        db.session.commit()
        if usuario is None:
            return "El usuario no existe", 404
        else:
            token_de_acceso = create_access_token(identity=usuario.id)
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso}, 200
        
class Ping (Resource):
    def get(self):
        return "pong", 200
    

class AddMail (Resource):
    @jwt_required()
    def post(self):
        try:
            email = request.json["email"]
            app = request.json["app_uuid"]
            
        except:
            return {"Message": "Diligencie todos los campos requeridos de la solicitud"}, 400
        user = UserMail.query.filter_by(email = email).all()
        if user:
            return {"Message": "El correo ya está registrado"}, 412
        else:
            try:
                motivo = request.json["blocked_reason"]
            except:
                motivo = ""
            fechaactual= datetime.now()
            ip = request.remote_addr
            new_user = UserMail(email=email, app=app,motivo= motivo, ip=ip, createdAt = fechaactual)
            db.session.add(new_user)
            db.session.commit()
            id_user = UserMail.query.filter_by(email = email).first()
            return {"El correo se agregó satisfactoriamente, el mail tiene id": id_user.id}, 201

class GetEmail (Resource):
    @jwt_required()
    def get(self, stremail):
        email_valid = UserMail.query.filter_by(email= stremail).first()
        
        if email_valid:
            return {"Encontrado": True, "Motivo": email_valid.motivo}, 200
        else:
            return {"Encontrado": False, "Motivo": "No encontrado el mail"}, 200

class JsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return JSONEncoder.default(self, obj)