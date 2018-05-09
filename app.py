import os
import sys
import jwt
import datetime
from flask_wtf import CsrfProtect
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_security import SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, Security
from werkzeug.security import generate_password_hash, check_password_hash

#Create app
app = Flask(__name__)
app.config.from_pyfile('config.py')

# Create database connection object
db = SQLAlchemy(app)

from views import *

if __name__=="__main__":
    app.run()