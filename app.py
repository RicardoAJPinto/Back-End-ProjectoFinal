import os
import sys
from flask_jwt_extended import (JWTManager, jwt_required, set_access_cookies, set_refresh_cookies, unset_jwt_cookies)
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
#from model import *
from views import *

#Create app
app = Flask(__name__)
app.config.from_pyfile('config.py')

# Create database connection object
db = SQLAlchemy(app)

jwt = JWTManager(app)

from views import *

if __name__=="__main__":
    app.run()