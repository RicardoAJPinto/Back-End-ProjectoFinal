import os
import sys
#import jwt
import datetime
import json
from flask_wtf.csrf import CSRFProtect
from functools import wraps
from flask import (Flask, render_template, request, redirect, url_for, 
                    jsonify, make_response, Blueprint)
from sqlalchemy_utils import JSONType
from flask_security import SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, Security, roles_required, roles_accepted
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_login import LoginManager, current_user    
from flask_admin import Admin ,BaseView, expose
from flask_admin.base import Admin, AdminIndexView, BaseView, MenuLink, expose
from flask_mail import Mail

# Create app
app = Flask(__name__)

# Configuration file   
app.config.from_pyfile('config.cfg')
# FIXME: isto esta a ser executado N vezes por causa dos imports
# random from app import *, devia ser corrigido.
# basta fazer o print(app.config) e ver que aparece N vezes

s = URLSafeTimedSerializer('Thisisasecret!')

# Create databas and admin page connection object
db = SQLAlchemy(app)
db.init_app(app)
admin = Admin(app)
login = LoginManager(app)
# Create database connection object

# class MyAdminIndexView(admin.AdminIndexView):
    
#     @expose('/')
#     def index(self):
#         if not login.current_user.is_authenticated():
#             return redirect(url_for('.login_view'))
#         return super(MyAdminIndexView, self).index()
# ,  index_view=MyAdminIndexView()
# @login.user_loader
# def load_user(user_id):
#     return User.query.get(user_id)

# class MyAdminIndexView(AdminIndexView):
#     def is_accessible(self):
#         return  current_user.is_authenticated and current_user.has_role('admin')

# admin = Admin(app, index_view=MyAdminIndexView())
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Swagger documentation
from swagger import *

# Authentication via other platforms
from OAuth import *
# Admin page
from AdminPage import *

from views import *
#from token import *
from api import * 
from pdf import *

# Normal run        -> app.run()
# HTTPS+cert+key    -> app.run(ssl_context=('cert.pem', 'key.pem'))
if __name__=="__main__":
<<<<<<< HEAD
    #app.run(debug=True, port=33507)
    app.run(host= '0.0.0.0')    # Normal run  
=======
    #app.run(debug=True, port=$PORT)
    port = int(os.environ.get('PORT', 5000))
    app.run(host= '0.0.0.0', port=port)    # Normal run  
>>>>>>> 99f529f... Heroku++
    # app.run( ssl_context=('cert.pem', 'key.pem'))    # HTTPS+cert+key
