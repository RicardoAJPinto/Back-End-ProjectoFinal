from app import app
from model import *
from flask import abort, request, send_file, send_from_directory, flash
from api import *
from flask_security import roles_required
from forms import UpdateAccountForm

from JsonWebToken import *

@app.route('/')
# @roles_required('Admin')
def home():
    return render_template('index.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def perfil():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.email = form.email.data 
        # current_user.api_key = form.email.api_key 
        db.session.commit()
        # flash('Your account has been updated', 'success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.api_key.data = current_user.api_key

    return render_template('profile.html', form=form)

@app.route('/login')
def change():
    return render_template('security/login_user.html')

@app.route('/test')
@login_required
def test():
    return render_template('layouts/layout2.html')

# Download file
@app.route('/return-file/')
def return_file():
    # mode a da para fazer append
    f = open('agent/config.py', 'w')
    print(current_user)
    insertAPIkey = str(current_user.api_key)
    f.write('headers= { "x-api-key":"'+ insertAPIkey + '"} \n')  # python will convert \n to os.linesep
    f.close()  # you can omit in most cases as the destructor will call it
    
    #key = User.query.filter_by(api_key=APIkey).first()
    #headers = {"x-api-key": "eiWee8ep9due4deeshoa8Peichai8Ei2"}
    
    return render_template('index.html')
    #return send_from_directory('agent', 'DetectOS.py', as_attachment=True)


###########################  Error 404 ############################>##
# I really need to explain this?
@app.errorhandler(404)
def page_not_found(e):
    #return make_response(jsonify({'error': 'Not found'}), 404)
    return render_template('404.html'), 404


###########################           Historico           #########################################

@app.route('/hist', methods=['POST'])
def createhist():
    data = request.get_json()
    hist = Historico(owner_id=data['owner'], name=data['name'], resultado=data['resultado'])
    db.session.add(hist) 
    db.session.commit()  
    return jsonify({'message' : 'New hist created!'})


#########################           Maquina             ###########################################


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
