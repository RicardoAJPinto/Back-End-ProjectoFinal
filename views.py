from app import app
from model import *
from flask import abort, request, send_file, send_from_directory, flash
from api import *
from forms import UpdateAccountForm, RequestResetForm, ResetPasswordForm
# importing required modules for zip
from zipfile import ZipFile
import os
 
from JsonWebToken import *
import itsdangerous

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/goreset')
# @roles_required('Admin')
def gogo():
    return render_template('resetpassword.html')

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
    return render_template('security/login_user.html')

@app.route('/reset_password', methods=['GET', 'POST'])
def resetpwd():
    return render_template('resetpassword.html')
    # form = RequestResetForm()
    # return render_template('resetpassword.html', form=form)

#<token> && token in parameter of the function
@app.route('/new_password/', methods=['GET', 'POST'])
def newpwd():
    form = ResetPasswordForm()
    return render_template('newpassword.html', form=form)
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.passowrd.data)
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! Now you are able to log in')
        return redirect(url_for('login'))


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
    
    # mode a da para fazer append
    # Insert API key from the authenticated user
    f = open('agent/config.py', 'w')
    print(current_user)
    insertAPIkey = str(current_user.api_key)
    f.write('headers= { "x-api-key":"'+ insertAPIkey + '"} \n')  # python will convert \n to os.linesep
    f.close()  # you can omit in most cases as the destructor will call it
    
    # Zip files
    get_all_file_paths('.\repos\Back-End-ProjectoFinal\agent')
    zipping()

    # Feature to add: Download zip/folder file 
    return send_from_directory('agent', 'Zeus-Agent.zip', as_attachment=True)

    ## Get input ##
    myfile="Zeus-Agent.zip"

    ## Try to delete the file ##
    try:
        os.remove(myfile)
    except OSError as e:  ## if failed, report it back to the user ##
        print ("Error: %s - %s." % (e.filename, e.strerror))

if __name__ == "__main__":
    main()

    # user_id='4'.encode('utf8')
    # with open('pubkey.pem', mode='rb') as pubfile:
    #     keydata = pubfile.read()
    #     pub_key = rsa.PublicKey.load_pkcs1(keydata)
    # encrypted = rsa.encrypt(user_id, pub_key)
    # user_64 = base64.b64encode(encrypted)
    # with open('agent/api.pem', mode='wb') as pubfile:
    #     pubfile.write(user_64)
    # return jsonify({'result':True})#send_from_directory('agent', 'zeus.py', as_attachment=True)

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
@token_required
def deletemachine(current_user):
    data = request.get_json()
    maq = machine.query.filter_by(machine=data['machine']).first()
    if not maq:
        return jsonify({'message' : 'No machine found!'})
    db.session.delete(maq)
    db.session.commit()
    return jsonify({'message' : 'The machine has been deleted!'})

@app.route('/addmachine', methods=['PUT']) 
def addmachine():
    data = request.get_json()
    machine = machine.query.filter_by(machine=data['mach']).first()
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


################################ Reset Password #################################

#users_blueprint = Blueprint('users', __name__, template_folder='templates')
    
@app.route('/reseted', methods=["POST"])
def reseted():
    form = RequestResetForm()
    try:
        user = User.query.filter_by(email=form.email.data).first()
    except:
        return render_template('password_reset_email.html', form=user.email)
         
    if user:
        s = URLSafeTimedSerializer('Thisisasecret!')
        token = s.dumps(user.email, salt='email-confirm')
        msg = Message('Confirm Email', sender='ZeusNoReply@gmail.com', recipients=[user.email])
        link = url_for('reset_with_token', token=token, _external=True)
        msg.body = 'Your link to new password is {}'.format(link)
        mail.send(msg)
    else:
        flash('Your email address must be confirmed before attempting a password reset.', 'error')
        return redirect(url_for('users.login'))
    return jsonify({'Result' : True})
 


@app.route('/confirm_email/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
        s = URLSafeTimedSerializer('Thisisasecret!')
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        return '<h1>The token is expired!</h1>'

    form = ResetPasswordForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=email).first_or_404()
        except:
            flash('Invalid email address!', 'error')
            return render_template('index.html')
        #generate_password_hash(form.password.data, method='sha256')
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return render_template('404.html')
 
    return render_template('newpassword.html', form=form, token=token)