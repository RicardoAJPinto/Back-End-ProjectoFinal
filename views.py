from app import app
from model import *


##############################################################################
# Views
##############################################################################

def token_required(f):  #Está fixe
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

            #token = token.split(' ')[1]
        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            #print("verificar o token: '", token, "' com a chave ", app.config['SECRET_KEY'], sep='')
            data = jwt.decode(token, app.config['SECRET_KEY'])
            #print("token verificado, user id: ", data['id'])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401
            
        #print('user returned: ', current_user)
        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/getme', methods=['GET'])
@token_required
def get(current_user):
    tkn = request.headers['x-access-token']
    user = User.query.filter_by(id=tkn.id)       #Não trabalha como deve ser
    return jsonify({identity})

@app.route('/user/<email>', methods=['DELETE'])    #Está fixe
@token_required
def delete(current_user, email):
    userdel = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message' : 'No user found!'})
    db.session.delete(userdel)
    db.session.commit()
    return jsonify({'message' : 'The user has been deleted!'})

@app.route('/users', methods=['GET'])   #Está fixe
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
    
@app.route('/profile/<email>')      #Está fixe
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

@app.route('/user123', methods=['POST']) #Está fixe
@token_required
def create(current_user):
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    user = User(email=data['email'],password=hashed_password)
    db.session.add(user) 
    db.session.commit()  
    return jsonify({'message' : 'New user created!'})


@app.route('/login123')  #Está fixe
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

@app.route('/protected', methods=['GET']) #Está fixe
@token_required
def protected(current_user):
    token = request.headers['x-access-token']
    return jsonify(token), 200