from views import *
from app import app
import requests
from forms import DeleteMachineForm
from model import *
import json 

@app.route('/quickstart')
@login_required
def quickstart():
    return render_template('dashboard/quickstart.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard/dashboard.html')

@app.route('/machines')
@login_required
def machines():
    # get_machines = request.get_json()
    # maq = Machine.query.filter_by(machine=get_machines['machine']).first()
    form = DeleteMachineForm()
    if form.validate_on_submit():
        # current_user.email = form.email.data 
        # db.session.commit()
        flash('The machine has been updated', 'success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.machine.data = current_user.email
        
    #url = 'https://zeus-security.herokuapp.com/api/scans' # Heroku
    url = 'http://127.0.0.1:5000/api/scans' # Local
    insertAPIkey = str(current_user.api_key)
    headers= { "x-api-key": insertAPIkey} 

    requestpost = requests.get(url , headers=headers).json()
    print(requestpost)
    json_size = len(requestpost["DetectOS"])
    print(json_size)
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
