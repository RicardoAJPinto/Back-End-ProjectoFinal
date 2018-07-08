from app import app, mail
from model import *
from flask import abort, request, send_file, send_from_directory, flash
from api import *
from forms import UpdateAccountForm, RequestResetForm, ResetPasswordForm
import os
from pdf import *
from smtp import *
import itsdangerous

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('index/about.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def perfil():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.email = form.email.data 
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.api_key.data = current_user.api_key

    return render_template('profile.html', form=form)

@app.route('/login')
def change():
    return render_template('security/login_user.html')

from dashboard import *

if __name__ == "__main__":
    main()

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
    hist = Historic(owner_id=data['owner'], name=data['name'], resultado=data['resultado'])
    db.session.add(hist) 
    db.session.commit()  
    return jsonify({'message' : 'New hist created!'})


#########################           Maquina             ###########################################
@app.route('/machine', methods=['POST']) 
def createmachine():
    data = request.get_json()
    hist = Machine(owner_id=data['owner'], machine_id=data['machine'])
    db.session.add(hist) 
    db.session.commit()  
    return jsonify({'message' : 'New machine created!'})

@app.route('/machine', methods=['DELETE'])   
@login_required
def deletemachine():

    maq = Machine.query.filter_by(id=form.machine.data).first()
    if not maq:
        return jsonify({'message' : 'No machine found!'})
    db.session.delete(maq)
    db.session.commit()
    return jsonify({'message' : 'The machine has been deleted!'})

@app.route('/addmachine', methods=['PUT']) 
def addmachine():
    data = request.get_json()
    machine = Machine.query.filter_by(machine=data['mach']).first()
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
