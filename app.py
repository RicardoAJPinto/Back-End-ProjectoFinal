import os
import sys
import jwt
import datetime
import json
from flask_wtf.csrf import CSRFProtect
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response, Blueprint
from sqlalchemy_utils import JSONType
from flask_security import SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, Security, roles_required, roles_accepted
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_login import LoginManager    
# Flask-admin 
from flask_admin import Admin ,BaseView, expose
from flask_admin.base import Admin, AdminIndexView, BaseView, MenuLink, expose
#from flask_debugtoolbar import DebugToolbarExtension 

# Create app
app = Flask(__name__)

#toolbar = DebugToolbarExtension()

# Configuration file   
app.config.from_pyfile('config.py')     

s = URLSafeTimedSerializer('Thisisasecret!')

# Enable toolbar on app
#toolbar.init_app(app)

# Create databas and admin page connection object
db = SQLAlchemy(app)
db.init_app(app)
admin = Admin(app)

# Swagger documentation
from swagger import *

# Authentication via other platforms
from OAuth import *
# Admin page
from AdminPage import *

from views import *
#from token import *
from api import * 

# app.run()
# HTTPS -> app.run(ssl_context=('cert.pem', 'key.pem'))
if __name__=="__main__":
    #app.run()
    app.run(ssl_context=('cert.pem', 'key.pem'))