from app import *
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required

##########################   User && Roles DB   ##########################
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    maquina = db.relationship('Maquina', backref='owner')
    historico = db.relationship('Historico', backref='owner')
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('userRole', lazy='dynamic'))

    # Flask-Login integration
    def is_authenticated(self):
        return True

##########################  xxxxx   ##########################
historico_Maquina = db.Table('historico_Maquina',
        db.Column('maquina_id', db.Integer(), db.ForeignKey('maquina.id')),
        db.Column('hist_id', db.Integer(), db.ForeignKey('historico.id')))

class Historico(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(80), unique=True)
    resultado = db.Column(db.String(255))

class Maquina(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    maquina = db.Column(db.String(255), unique=True)
    roles = db.relationship('Historico', secondary=historico_Maquina,
                            backref=db.backref('maqHist', lazy='dynamic'))


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('maquina.id'))
    dataos = db.Column(JSONType)

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Create a user to test with 
# Runs 1 time
# @app.before_first_request
# def create_user():
#     db.create_all()
#     user_datastore.create_user(email='test@test.test', password=encrypt_password('test1234'))
#     db.session.commit()
