from app import db, admin
from flask_admin import Admin 
from flask_admin.contrib.sqla import ModelView 
import os.path as op
from flask_admin import Admin ,BaseView, expose
from flask_login import LoginManager, current_user  

# Commnad line for admin interface
from redis import Redis
from flask_admin.contrib import rediscli

from model import User, Role, Historic
class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role('admin')

admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Role, db.session))
admin.add_view(AdminView(Historic, db.session))