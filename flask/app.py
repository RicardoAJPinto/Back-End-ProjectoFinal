import os
import sys
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
from flask_mail import Mail, Message
import flask_login
from werkzeug.utils import secure_filename

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

# login = LoginManager(app)
login_manager = LoginManager()
login_manager.login_view = 'github.login'
login_manager.init_app(app)

# class MyAdminIndexView(AdminIndexView):    
#     @expose('/')
#     def index(self):
#         if not current_user.is_authenticated:
#             return redirect(url_for('.login_view'))
#         return super( (MyAdminIndexView, self).index(),  index_view = MyAdminIndexView() )


# @login.user_loader
# def load_user(user_id):
#     return User.query.get(user_id)

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return  current_user.is_authenticated and current_user.has_role('admin')
<<<<<<< HEAD:app.py

admin = Admin(app, index_view=MyAdminIndexView())
# OAuth config
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
mail = Mail(app)
=======

#and current_user.has_role('admin')
admin = Admin(app, index_view=MyAdminIndexView())

# OAuth config
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

mail = Mail(app)

>>>>>>> master:flask/app.py
# Authentication via other platforms
from OAuth import *
# Admin page
from AdminPage import *

from views import *
from api import * 
from pdf import *

if __name__=="__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host= '0.0.0.0', port=port)    # Normal run  
    # app.run( ssl_context=('cert.pem', 'key.pem'))    # HTTPS+cert+key
