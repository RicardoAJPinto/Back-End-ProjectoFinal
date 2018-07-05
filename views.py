from app import app, mail
from model import *
from flask import abort, request, send_file, send_from_directory, flash
from api import *
from forms import UpdateAccountForm, RequestResetForm, ResetPasswordForm
# importing required modules for zip
from zipfile import ZipFile
import os
from smtp import *
from JsonWebToken import *
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
        # current_user.api_key = form.email.api_key 
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.api_key.data = current_user.api_key

    return render_template('profile.html', form=form)

@app.route('/login')
def change():
    test = Test(DetectOS=True, NewScan=True)
    db.session.add(test)
    db.session.commit()
    return render_template('security/login_user.html')

from dashboard import *

# Download file
@app.route('/return-file/')
def return_file():
    def get_all_file_paths(directory):
        # initializing empty file paths list
        file_paths = []

        # crawling through directory and subdirectories
        for root, directories, files in os.walk(directory):
            for filename in files:
                # join the two strings in order to form the full filepath.
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)

        ## Try to delete the file ##
        try:
            os.remove("./agent/Zeus-Agent.zip")
            #os.remove("./agent/NewScan.py")
        except OSError as e:  ## if failed, report it back to the user ##
            print ("Error: %s - %s." % (e.filename, e.strerror))

        # returning all file paths
        return file_paths        

    def zipping():
        # path to folder which needs to be zipped
        directory = './agent'

        # calling function to get all file paths in the directory
        file_paths = get_all_file_paths(directory)

        # printing the list of all files to be zipped
        print('Following files will be zipped:')
        for file_name in file_paths:
            print(file_name)

        # writing files to a zipfile
        with ZipFile('agent/Zeus-Agent.zip','w') as zip:
            # writing each file one by one
            for file in file_paths:
                zip.write(file)

        print('All files zipped successfully!')    
    
    # Insert API key from the authenticated user
    insertAPIkey = str(current_user.api_key)

    apikey = insertAPIkey.encode('utf8')
    with open('pubkey.pem', mode='rb') as pubfile:
        keydata = pubfile.read()
        pub_key = rsa.PublicKey.load_pkcs1(keydata)
    encrypted = rsa.encrypt(apikey, pub_key)
    user_64 = base64.b64encode(encrypted)
    with open('agent/api.pem', mode='wb') as pubfile:
        pubfile.write(user_64)

    # Zip files
    get_all_file_paths('.\repos\Back-End-ProjectoFinal\agent')
    zipping()

    # Feature to add: Download zip/folder file 
    return send_from_directory('agent', 'Zeus-Agent.zip', as_attachment=True)

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
    hist = Historico(owner_id=data['owner'], name=data['name'], resultado=data['resultado'])
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
    form = DeleteMachineForm()
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
