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
    #return render_template('dashboard/Inspirationexample.html', APIcall=requestpost, json_size=json_size)
    #return render_template('dashboard/Inspirationexample.html', APIcall=requestpost, json_size=json_size)

# @app.route('/reloads')
# @login_required
# def reload_test():
#     form = UpdateAccountForm()
#     if form.validate_on_submit():
#         test = Test.query.filter_by(id=current_user.test_id).first()
#         if not test.DetectOS == form.DetectOS:
#             test2 = Test.query.filter_by(DetectOS=form.DetectOS)
#             if not test2:
#                 test = Test(DetectOS=DetectOS)
#                 db.session.add(test) 
#                 db.session.commit()
#         try:
#             current_user.test_id = test.id
#             db.session.commit()
#         except:
#             abort(404)
#     return jsonify({'Scan_added': True}), 201

@app.route('/create1', methods=['POST'])
def create1():

    test = Test(DetectOS=True, AV=False)
    
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
    if not user:
        abort(400)
    test = Test.query.filter_by(id=user.test_id).first()
    payload2 = {}
    payload2["DetectOS:"] = test.DetectOS
    print(test.AV)
    payload2["AV:"] = test.AV

    payload = json.dumps(payload2)
    return payload
