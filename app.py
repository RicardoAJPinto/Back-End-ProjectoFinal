import os
import sys
import jwt
import datetime
import json
from flask_wtf import CsrfProtect
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import JSONType
from flask_security import SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, Security
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_login import LoginManager

#Create app
app = Flask(__name__)
app.config.from_pyfile('config.py')

mail = Mail(app)
s = URLSafeTimedSerializer('Thisisasecret!')

# Create database connection object
db = SQLAlchemy(app)

from views import *
from api import * 

if __name__=="__main__":
    app.run()


    