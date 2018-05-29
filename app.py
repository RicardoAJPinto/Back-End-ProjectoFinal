import os
import sys
import jwt
import datetime
from flask_wtf import CsrfProtect
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy # DB
from flask_security import SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, Security, roles_required, roles_accepted
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_login import LoginManager    

from flask_admin import Admin ,BaseView, expose
from flask_admin.base import Admin, AdminIndexView, BaseView, MenuLink, expose

# Create app
app = Flask(__name__)
# Configuration file   
app.config.from_pyfile('config.py')     

s = URLSafeTimedSerializer('Thisisasecret!')

# Create database connection object
db = SQLAlchemy(app)

# # Create customized model view class
# class MyModelView(sqla.ModelView):

#     def is_accessible(self):
#         return login.current_user.is_authenticated()

# class MyAdminIndexView(admin.AdminIndexView):
    
#     @expose('/')
#     def index(self):
#         if not login.current_user.is_authenticated():
#             return redirect(url_for('.login_view'))
#         return super(MyAdminIndexView, self).index()
# ,  index_view=MyAdminIndexView()
admin = Admin(app)

from AdminPage import *

from views import *
from api import * 

if __name__=="__main__":
    app.run()