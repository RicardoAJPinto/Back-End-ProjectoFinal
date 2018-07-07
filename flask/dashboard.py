from views import *
from app import app
from api import *
import requests
from forms import DeleteMachineForm
from model import *
import json 
from pdf import generate_pdf

@app.route('/quickstart')
@login_required
def quickstart():
    return render_template('dashboard/quickstart.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard/dashboard.html')

@app.route('/machines_del', methods=['POST'])
def machines_del():
    mach = request.form.get('machine_id')
    print(mach)
    machine = Machine.query.filter_by(machine_id=mach).first()
    if not machine:
        abort(404)
    db.session.delete(machine)
    db.session.commit()
    return redirect(url_for('perfil'))

@app.route('/machines')
@login_required
def machines():
    form = DeleteMachineForm()
    #url = 'https://zeus-security.herokuapp.com/api/scans' # Heroku
    url = 'http://127.0.0.1:5000/api/scans' # Local
    #insertAPIkey = str(current_user.api_key)
    #headers= { "x-api-key": insertAPIkey} 

    requestpost, json_size = get_scans() #requests.get(url).json(), headers=headers
    return render_template('dashboard/HistoryMachines.html', form=form, APIcall=requestpost, json_size=json_size)
    

# if request.method == 'GET':
#     xxx
# elif request.method == 'POST':

@app.route('/receiver', methods = ['GET','POST'])
def worker():
    if not request.json:
        abort(400)
    print(request.json)
    return json.dumps(request.json)
    

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

    if len(jsonObjectInfo['checkedItems']) == 1:
        test = Test(**{DetectOS:True}, **{NewScan:False} )
        db.session.add(test) 
        db.session.commit()
    else:
        size = 1
        for i in range(size):
            ActivatedDet = jsonObjectInfo['checkedItems'][i]
            ActivatedNew = jsonObjectInfo['checkedItems'][i+1]
            print(ActivatedDet)
            print(ActivatedNew)
            #Gets the activated test and put it on DB
            # Same as (**{DetectOS:True}, **{NewScan:True} )
            test = Test(**{ActivatedDet:True}, **{ActivatedNew:True} )
            db.session.add(test) 
            db.session.commit()
            return jsonify({'Scan_added':True}), 201


@app.route('/reload', methods=['GET'])
def reload_agent():
    with open('keye.pem', mode='rb') as privfile:
        keydata = privfile.read()
        priv_key = rsa.PrivateKey.load_pkcs1(keydata)
    
    if not 'user-id' in request.headers:
        abort(400)
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
