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
    machine = db.relationship('Machine', backref='owner')
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('userRole', lazy='dynamic'))

    # Flask-Login integration
    def is_authenticated(self):
        return current_user.is_authenticated()

##########################  xxxxx   ##########################

class Historic(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    machine_id = db.Column(db.Integer, db.ForeignKey('machine.id'))
    dataos = db.Column(JSONType)

class Machine(db.Model, UserMixin): 
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    machine_id = db.Column(db.String(255), unique=True)
    history = db.relationship('Historic', backref='owner')


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Create a user to test with 
# Runs 1 time
@app.before_first_request
def create_user():
    db.create_all()
    #user_datastore.create_user(email='test@test.test', password='test1234')
    db.session.commit()
