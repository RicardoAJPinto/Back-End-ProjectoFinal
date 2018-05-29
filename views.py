from app import app
from model import *
from api import *
from flask import abort, request

##########################      Validação Token         ##############

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

##############################################################################
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

#########################       Get UserID from Token

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

###############################         Delete User     #####################
@app.route('/user/<email>', methods=['DELETE'])    #Está fixe
@token_required
def delete(current_user, email):
    userdel = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message' : 'No user found!'})
    db.session.delete(userdel)
    db.session.commit()
    return jsonify({'message' : 'The user has been deleted!'})

####################################        Profile / All user
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

##############################          Registo / Auth
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

################################    Test Token          ################################>
@app.route('/protected', methods=['GET']) #Está fixe
@token_required
def protected(current_user):
    token = request.headers['x-access-token']
    return jsonify(token), 200


###########################  Error 404 ############################>##
# I really need to explain this?
@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({'error': 'Not found'}), 404)
    #return render_template('404.html'), 404

###########################           Histórico           #########################################

@app.route('/hist', methods=['POST'])
def createhist():
    data = request.get_json()
    hist = Historico(owner_id=data['owner'], name=data['name'], resultado=data['resultado'])
    db.session.add(hist) 
    db.session.commit()  
    return jsonify({'message' : 'New hist created!'})


#########################           Máquina             ###########################################


@app.route('/maquina', methods=['POST']) 
def createmaquina():
    data = request.get_json()
    hist = Maquina(owner_id=data['owner'], maquina=data['maquina'])
    db.session.add(hist) 
    db.session.commit()  
    return jsonify({'message' : 'New machine created!'})

@app.route('/maquina', methods=['DELETE'])   
@token_required
def deleteMaquina(current_user):
    data = request.get_json()
    maq = Maquina.query.filter_by(maquina=data['maquina']).first()
    if not maq:
        return jsonify({'message' : 'No machine found!'})
    db.session.delete(maq)
    db.session.commit()
    return jsonify({'message' : 'The machine has been deleted!'})

@app.route('/addMaquina', methods=['PUT']) 
def addMaquina():
    data = request.get_json()
    machine = Maquina.query.filter_by(maquina=data['mach']).first()
    if not machine:
        return jsonify({'message' : 'No machine found!'})
    hist = Historico.query.filter_by(name=data['histo']).first()
    if not hist:
        return jsonify({'message' : 'No history found!'})
    machine.roles.append(hist)
    db.session.commit()
    return jsonify({'message' : 'Machine added with history!'})


#######################             Roles           #########################################

@app.route('/role', methods=['POST'])
def createRole():
    data = request.get_json()
    role = Role(name=data['name'])
    db.session.add(role) 
    db.session.commit()  
    return jsonify({'message' : 'New role created!'})

@app.route('/role', methods=['DELETE'])   
@token_required
def deleteRole(current_user):
    data = request.get_json()
    role = Role.query.filter_by(name=data['name']).first()
    if not role:
        return jsonify({'message' : 'No role found!'})
    db.session.delete(role)
    db.session.commit()
    return jsonify({'message' : 'The role has been deleted!'})


@app.route('/role', methods=['POST']) 
def addRole():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'message' : 'No user found!'})
    role = Role.query.filter_by(name=data['role']).first()
    if not role:
        return jsonify({'message' : 'No role found!'})
    user.roles.append(role)
    db.session.commit()
    return jsonify({'message' : 'Role added to user!'})

######################### API #########################
# Get all the scans
@app.route('/api/scans', methods=['GET'])
def get_scans():

    result = Result.query.all() 
    output = []
    for result in result:
        out = {}
        out['id'] = result.id
        out['dataos'] = result.dataos
        output.append(out)

    return jsonify({'Results' : output})
    #return jsonify({'DetectOS': [make_public_DetectOS(scan) for scan in DetectOS]})


# Get the scan passing the ID on the route
@app.route('/api/scans/<int:scan_id>', methods=['GET'])
def get_scanid(scan_id):
    scan = Result.query.filter_by(id=scan_id).first()
    if not scan:
        return jsonify({'message' : 'No scan found!'})
    out = {}
    out['id'] = result.id
    out['dataos'] = result.dataos
    return jsonify({'Output' : out})

    # scan = [scan for scan in DetectOS if scan['id'] == scan_id]
    # if len(scan) == 0:
    #     abort(404)
    # return jsonify({'scan': scan[0]})

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
    result = Result(owner_id = 1)
    result.dataos = new_scan
    db.session.add(result) 
    db.session.commit()
    return jsonify({'Scan_added': new_scan}), 201

# Update a parameter passing the id on the route
@app.route('/api/scans/<int:scan_id>', methods=['PUT'])
def update_scan(scan_id):
    #scan = [scan for scan in DetectOS if scan['id'] == scan_id]
    scan = Result.query.filter_by(id=scan_id).first()
    if not scan:
        abort(404)
    if not request.json:
        abort(400)
    if 'machine' in request.json and type(request.json['machine']) != str:
        abort(400)
    if 'node' in request.json and type(request.json['node']) != str:
        abort(400)
    if 'processor' in request.json and type(request.json['processor']) != str:
        abort(400)
    if 'release' in request.json and type(request.json['release']) != str:
        abort(400)
    if 'system' in request.json and type(request.json['system']) != str:
        abort(400)
    if 'version' in request.json and type(request.json['version']) != str:
        abort(400)

    scan.dataos['machine'] = request.json.get('machine', scan.dataos['machine']) 
    scan.dataos['node'] = request.json.get('node', scan.dataos['node']) 
    scan.dataos['processor'] = request.json.get('processor', scan.dataos['processor']) 
    scan.dataos['release'] = request.json.get('release', scan.dataos['release']) 
    scan.dataos['system'] = request.json.get('system', scan.dataos['system']) 
    scan.dataos['version'] = request.json.get('version', scan.dataos['version']) 


    scan.dataos['machine'][ request.json.get('machine')]
    db.session.commit()
    return jsonify({'Scan_added': scan.id}), 201


@app.route('/api/scans/<int:scan_id>', methods=['DELETE'])
def delete_scan(scan_id):
    scan = Result.query.filter_by(id=scan_id).first()
    if not scan:
        return jsonify({'message' : 'No machine found!'})
    db.session.delete(scan)
    db.session.commit()
    return jsonify({'result': True})

