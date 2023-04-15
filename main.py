from tokenize import String
from flask import request, jsonify, Flask
from flask_jwt_extended import jwt_required, create_access_token,get_jwt, JWTManager, get_jwt_identity
from flask_restful import Resource, Api
# from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
import decimal
import json
from flask.json import JSONEncoder
from flask import current_app as app
import os
import jwt
from modelo import User, db
from datetime import datetime, timedelta
from vistas.vistas import Ping, VistaSignIn, VistaLogIn, AddMail, GetEmail

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baseListaNegra.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True


app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)

api.add_resource(VistaSignIn, '/users/')
api.add_resource(VistaLogIn, '/users/auth')
api.add_resource(Ping, '/users/ping')
api.add_resource(AddMail, '/blacklists')
api.add_resource(GetEmail, '/blacklists/<string:stremail>')


jwt = JWTManager(app)

  