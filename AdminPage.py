from app import db, admin
from flask_admin import Admin 
from flask_admin.contrib.sqla import ModelView 
from flask_admin.contrib.fileadmin import FileAdmin
import os.path as op
from flask_admin import Admin ,BaseView, expose

# Commnad line for admin interface
from redis import Redis
from flask_admin.contrib import rediscli

from model import User, Role
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Role, db.session))
path = op.join(op.dirname(__file__), 'static')
admin.add_view(FileAdmin(path, '/static/', name='Static Files'))
admin.add_view(rediscli.RedisCli(Redis()))  #cmd