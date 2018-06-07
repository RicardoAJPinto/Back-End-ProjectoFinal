from app import app
from model import *
from flask import abort, request, send_file, send_from_directory, flash

##########################   Decorators   ##########################   
# Decorator to validate token
def token_required(f):  
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401
        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)

    return decorated

 
@app.route('/getme', methods=['GET'])
@token_required
def get(current_user):
    try: 
        token = request.headers['x-access-token']
        data = jwt.decode(token, app.config['SECRET_KEY'])
        userr = User.query.filter_by(id=data['id']).first()
    except:
        return jsonify({'message' : 'Token is 123!'}), 401     
    return jsonify({'user' : userr.id})

####################################        Profile / All user
@app.route('/users', methods=['GET'])   
@token_required
def show(current_user):
    user = User.query.all() 
    output = []
    for user in user:
        user_data = {}
        user_data['id'] = user.id
        user_data['email'] = user.email
        user_data['password'] = user.password
        output.append(user_data)

    return jsonify({'users' : output})
    
@app.route('/profile/<email>')      
@token_required
def profile(current_user, email):
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message' : 'No user found!'})

    user_data = {}
    user_data['id'] = user.id
    user_data['email'] = user.email
    user_data['password'] = user.password

    return jsonify({'user' : user_data})

##############################          Registo / Auth
@app.route('/user123', methods=['POST']) 
def create():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    user = User(email=data['email'],password=hashed_password)
    db.session.add(user) 
    db.session.commit()  
    return jsonify({'message' : 'New user created!'})


@app.route('/login123') 
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(email=auth.username).first()

    if not user:
        return make_response('Could not 2', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not 3', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

###############################         Delete User     #####################
@app.route('/user/<email>', methods=['DELETE'])    
@token_required
def delete(current_user, email):
    userdel = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message' : 'No user found!'})
    db.session.delete(userdel)
    db.session.commit()
    return jsonify({'message' : 'The user has been deleted!'})

################################    Test Token          ################################>
@app.route('/protected', methods=['GET']) 
@token_required
def protected(current_user):
    token = request.headers['x-access-token']
    return jsonify(token), 200
