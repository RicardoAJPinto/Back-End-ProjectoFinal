import os
import sys
from flask_jwt_extended import (JWTManager, jwt_required, set_access_cookies, set_refresh_cookies, unset_jwt_cookies)
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from model import *

#check Block tags - importante para poupar linhas de codigo 

#Create app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/projetofinal'
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_REGISTERABLE'] = True
#Set the application in debug mode so that the server is reloaded on any code change & helps debug
app.config['DEBUG'] = True

app.config['JWT_TOKEN_LOCATION'] = ['cookies']
#app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_SECRET_KEY'] = 'abva'

app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
app.config['SECURITY_PASSWORD_SALT'] = '$2a$16$PnnIgfMwkOjGX4SkHqSOPO'

# Create database connection object
db = SQLAlchemy(app)

jwt = JWTManager(app)
# Define models
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
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))



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


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add')
def add():
    return render_template('add_user.html')

@app.route('/delete', methods=['POST'])
@login_required
def delete():
    userdel = User.query.filter_by(id=request.form['id']).first()
    db.session.delete(userdel)
    db.session.commit()
    user = User.query.all()
    return render_template('show.html', user=user)


@app.route('/show')
@login_required
def show():
    user = User.query.all() 
    return render_template('show.html', user=user)

@app.route('/token/auth', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = User.query.all()
    for user in user: 
        if user.email == email and user.password == password:
            access_token = create_access_token(identity=user.email)
            refresh_token = create_refresh_token(identity=user.email)
            # Set the JWTs and the CSRF double submit protection cookies
            # in this response
            resp = jsonify({'login': True})
            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)
            return resp, 200
                    
             
    return jsonify({'login': False}), 401  
    
    
@app.route('/profile/<email>')
@login_required
def profile(email):
    user = User.query.filter_by(email=email).first()
    return render_template('profile.html',  user=user)

@app.route('/post_user', methods=['POST'])
def post_user():
    user = User(email=request.form['email'], password=request.form['password'])
    db.session.add(user) #add object
    db.session.commit()  #save 
    return redirect(url_for('index'))

@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    ret = {
        'current_identity': get_jwt_identity(),  # test
    }
    return jsonify(ret), 200


@app.route('/token/remove', methods=['POST'])
def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200

if __name__=="__main__":
    app.run()