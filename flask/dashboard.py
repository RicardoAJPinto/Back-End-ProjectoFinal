from views import *
from app import app, db
from api import *
import requests
from forms import DeleteMachineForm
from model import *
import json 
from pdf import generate_pdf
# importing required modules for zip
from zipfile import ZipFile

@app.route('/quickstart')
@login_required
def quickstart():
    return render_template('dashboard/quickstart.html')
 
@app.route('/dashboard')
@login_required
def dashboard():
    form = DeleteMachineForm()
    
    requestpost, count_all, count, count_win, count_lin = get_scans_table()
    mach = Machine.query.filter_by(owner_id=current_user.id).distinct()
    requestpost, json_size = get_scans()
    return render_template('dashboard/dashboard.html', form=form, APIcall=requestpost, json_size=json_size, count=count, count_win=count_win, count_lin=count_lin)

# ################################# File upload Section #################################
#File upload
UPLOAD_FOLDER = 'agent/'
ALLOWED_EXTENSIONS = set(['py'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']

    # Colocar nome com currentuser
    if file and allowed_file(file.filename):
        #file.save(os.path.join('agent/', current_user.email + "NewScan.py"  ))
        file.save(os.path.join('agent/', "NewScan.py"))

    # CHANGE THIS! NO HARDCODE MODE XD !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return render_template("dashboard/quickstart.html")
    # return jsonify({'message' : 'File uploaded!'}), 201

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

        ## Delete existing files ##
        try:
            os.remove("./agent/Zeus-Agent.zip")
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

        ## Delete existing files ##
        try:
            os.remove("./agent/NewScan.py")
        except OSError as e:  ## if failed, report it back to the user ##
            print ("Error: %s - %s." % (e.filename, e.strerror))

        print('All files zipped successfully!')    
    
    # Insert API key from the authenticated user
    insertAPIkey = str(current_user.api_key)

    apikey = insertAPIkey.encode('utf8')
    with open('flask/pubkey.pem', mode='rb') as pubfile:
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
    return send_from_directory('../agent', 'Zeus-Agent.zip', as_attachment=True)

@app.route('/machines_del', methods=['POST'])
def machines_del():
    mach = request.form.get('machine_id')
    print(mach)
    machine = Machine.query.filter_by(machine_id=mach).first()
    if not machine:
        abort(404)
    db.session.delete(machine)
    db.session.commit()
    return redirect(url_for('machines'))
 
@app.route('/machines')
@login_required
def machines():

    url = 'https://zeus-sec.herokuapp.com/api/scans' # Heroku
    #url = 'http://127.0.0.1:5000/api/scans' # Local
    #insertAPIkey = str(current_user.api_key)
    #headers= { "x-api-key": insertAPIkey} 
 
    requestpost, json_size = get_scans() #requests.get(url).json(), headers=headers
 
    return render_template('dashboard/HistoryMachines.html', APIcall=requestpost, json_size=json_size)
     
@app.route('/create1', methods=['POST'])
def create1():
    if not request.json:
        abort(400)
    
    jsonObjectInfo = request.json
    print(type(jsonObjectInfo))
    print(jsonObjectInfo)

    print("Array is {0}".format(jsonObjectInfo['checkedItems']))
    #If more scans or more buttons are added, add this:
    # size = len(jsonObjectInfo['checkedItems'])
    # print(size)

    testset = Test.query.filter_by(id=current_user.test_id).first() 

    if len(jsonObjectInfo['checkedItems']) == 1:
        #test = Test(DetectOS=True, NewScan=False )
        testset.DetectOS = True
        testset.NewScan = False
        #db.session.add(test) 
        db.session.commit()
        return jsonify({'Scan_added':True}), 201
    else:
        size = 1
        for i in range(size):
            ActivatedDet = jsonObjectInfo['checkedItems'][i]
            ActivatedNew = jsonObjectInfo['checkedItems'][i+1]
            print(ActivatedDet)
            print(ActivatedNew)
            #Gets the activated test and put it on DB
            # Same as (**{DetectOS:True}, **{NewScan:True} )
            #test = Test(**{ActivatedDet:True}, **{ActivatedNew:True} )
            #db.session.add(test) 
            testset.DetectOS = True 
            testset.NewScan = True
            db.session.commit()
            return jsonify({'Scan_added':True}), 201


@app.route('/reload', methods=['GET'])
def reload_agent():
    with open('flask/keye.pem', mode='rb') as privfile:
        keydata = privfile.read()
        priv_key = rsa.PrivateKey.load_pkcs1(keydata)
    
    if not 'user-id' in request.headers:
        abort(401)
    usernode = request.headers.get('user-id')
    message_id = base64.b64decode(usernode)
    user_id = rsa.decrypt(message_id, priv_key)
    message_user = user_id.decode('utf8')
 
    user = User.query.filter_by(api_key=message_user).first()
    # if not user:
    #     abort(400)
    #test = Test.query.filter_by(id=user.test_id).first()
    test = Test.query.filter_by(id=Test.id).first()
    payload2 = {}
    payload2["DetectOS:"] = test.DetectOS
    print(test.DetectOS)
    payload2["NewScan:"] = test.NewScan
    print(test.NewScan)
 
    payload = json.dumps(payload2)
    return payload