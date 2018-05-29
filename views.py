from app import app
from model import *
from flask import abort, request, send_file, send_from_directory
from api import *
from flask_security import roles_required

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

#######################################################################

@app.route('/')
# @roles_required('Admin')
def home():
    return render_template('index.html')

# @app.route('/administrator')
# @login_required
# def admin():
#     return render_template('admin/index.html')

@app.route('/profile')
@login_required
def perfil():
    return render_template('profile.html')

@app.route('/login')
def change():
    return render_template('security/login_user.html')

@app.route('/test')
@login_required
def test():
    return render_template('layouts/layout2.html')

# Download file(it will not work if you will run zeus.py)
@app.route('/return-file/')
def return_file():
    return send_from_directory('agent', 'zeus.py', as_attachment=True)

@app.route('/getme', methods=['GET'])
@token_required
def get(current_user):
    tkn = request.headers['x-access-token']
    user = User.query.filter_by(id=tkn.id)       #Não trabalha como deve ser
    return jsonify({identity})

###########################  Error 404 ############################>##
# I really need to explain this?
@app.errorhandler(404)
def page_not_found(e):
    #return make_response(jsonify({'error': 'Not found'}), 404)
    return render_template('404.html'), 404

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


@app.route('/addRole', methods=['POST']) 
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
