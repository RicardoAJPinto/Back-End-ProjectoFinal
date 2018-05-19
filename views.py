from app import app
from model import *
from api import *
from flask import abort, request

def token_required(f):  #Está fixe (TOPPPP)
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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/profile')
@login_required
def perfil():
    return render_template('profile.html')

@app.route('/login')
def change():
    return render_template('security/login_user.html')

@app.route('/test')
def test():
    return render_template('layouts/layout2.html')

@app.route('/getme', methods=['GET'])
@token_required
def get(current_user):
    tkn = request.headers['x-access-token']
    user = User.query.filter_by(id=tkn.id)       #Não trabalha como deve ser
    return jsonify({identity})

#Delete user
@app.route('/user/<email>', methods=['DELETE'])    #Está fixe
@token_required
def delete(current_user, email):
    userdel = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message' : 'No user found!'})
    db.session.delete(userdel)
    db.session.commit()
    return jsonify({'message' : 'The user has been deleted!'})

#Show data from current user logged
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

#Adiciona novo utilizador
@app.route('/user123', methods=['POST']) #Está fixe
def create():
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

# I really need to explain this?
@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({'error': 'Not found'}), 404)
    #return render_template('404.html'), 404

######################### API #########################
# Get all the scans
@app.route('/api/scans', methods=['GET'])
def get_scans():
    return jsonify({'DetectOS': [make_public_DetectOS(scan) for scan in DetectOS]})

# Get the scan passing the ID on the route
@app.route('/api/scans/<int:scan_id>', methods=['GET'])
def get_scanid(scan_id):
    scan = [scan for scan in DetectOS if scan['id'] == scan_id]
    if len(scan) == 0:
        abort(404)
    return jsonify({'scan': scan[0]})

# Post a new scan to the API
@app.route('/api/scans', methods=['POST'])
def post_scan():
    if not request.json or not 'system' or not 'version' in request.json:
        abort(400)
    new_scan = {
        'id': DetectOS[-1]['id'] + 1,  
        'machine': request.json.get('machine', ""),
        'node': request.json.get('node', ""),
        'processor': request.json.get('processor', "" ),
        'release': request.json.get('release', ""),
        'system': request.json['system'],
        'version': request.json['version']
    }
    DetectOS.append(new_scan)
    return jsonify({'Scan_added': new_scan}), 201

# Update a parameter passing the id on the route
@app.route('/api/scans/<int:scan_id>', methods=['PUT'])
def update_scan(scan_id):
    scan = [scan for scan in DetectOS if scan['id'] == scan_id]
    if len(scan) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'machine' in request.json and type(request.json['machine']) != str:
        abort(400)
    if 'node' in request.json and type(request.json['node']) != str:
        abort(400)
    if 'processor' in request.json and type(request.json['processor']) !=str:
        abort(400)
    if 'release' in request.json and type(request.json['release']) != str:
        abort(400)
    if 'system' in request.json and type(request.json['system']) != str:
        abort(400)
    if 'version' in request.json and type(request.json['version']) != str:
        abort(400)

    scan[0]['machine'] = request.json.get('machine', scan[0]['machine'])
    scan[0]['node'] = request.json.get('node', scan[0]['node'])
    scan[0]['processor'] = request.json.get('processor', scan[0]['processor'])
    scan[0]['release'] = request.json.get('release', scan[0]['release'])
    scan[0]['system'] = request.json.get('system', scan[0]['system'])
    scan[0]['version'] = request.json.get('version', scan[0]['version'])
    return jsonify({'Updated_scan': scan[0]})


@app.route('/api/scans/<int:scan_id>', methods=['DELETE'])
def delete_scan(scan_id):
    scan = [scan for scan in DetectOS if scan['id'] == scan_id]
    if len(scan) == 0:
        abort(404)
    DetectOS.remove(scan[0])
    return jsonify({'result': True})

