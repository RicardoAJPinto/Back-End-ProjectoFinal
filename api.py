from app import *
from flask_restful import Resource, Api
from json import dumps
from flask import jsonify, url_for, abort, request
from model import User
from model import Historic, Machine
import ast
import rsa
import base64

DetectOS = [
    {
        'id': 1,
        "system": "Windows",
        "node": "Mr-Sequeira",
        "release": "10",
        "version": "10.0.17134",
        "machine": "AMD64",
        "processor": "Intel64 Family 6 Model 69 Stepping 1, GenuineIntel"
    },
    {
        'id': 2,
        "system": "Linux",
        "node": "xxxxxx",
        "release": "xxxxx",
        "version": "xxxx",
        "machine": "xxxxx",
        "processor": "Intel64 Family 6 Model 69 Stepping 1, GenuineIntel"
    }
]

# To test:
#    -curl http://127.0.0.1:5000/api/scans
#    -curl -v -H "x-api-key: eiWee8ep9due4deeshoa8Peichai8Ei2" http://127.0.0.1:5000/api/scans 
######################### Decorators #################################
# API key validation
def require_appkey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        APIkey = None
        if 'x-api-key' in request.headers:
            APIkey = request.headers.get('x-api-key')
        if not APIkey:
            return jsonify({'message' : 'APIKey is missing!'}), 401
        print(APIkey)
        try:
            key = User.query.filter_by(api_key=APIkey).first()
            print(key)
        except:
            return jsonify({'message' : 'APIKey is invalid!'}), 401
        return view_function(key, *args, **kwargs)
    return decorated_function


########################## REAL GENERATE PRIVATE KEY   (on comand line)
   # openssl genrsa -out key.pem
   # openssl rsa -in key.pem -RSAPublicKey_out -out pubkey.pem


@app.route('/generatetest', methods=['GET'])
def generate_keytest():

    with open('pubkey.pem', mode='rb') as pubfile:
        keydata = pubfile.read()
    pub = rsa.PublicKey.load_pkcs1(keydata)
    user_id = '4'.encode('utf8')
    encrypted = rsa.encrypt(user_id, pub)
    return jsonify({'result': True })
######################### API views ###################################
# encode - decode -
# Get all the scans
@app.route('/api/scans', methods=['GET'])
@require_appkey
def get_scans(user):
    return jsonify({'DetectOS': [make_public_DetectOS(scan) for scan in DetectOS]})

# Get the scan passing the ID on the route
@app.route('/api/scans/<int:scan_id>', methods=['GET'])
def get_scanid(scan_id):
    result = Historic.query.filter_by(id=scan_id).first()
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
# @require_appkey
def post_scan():
    with open('keye.pem', mode='rb') as privfile:
        keydata = privfile.read()
        priv_key = rsa.PrivateKey.load_pkcs1(keydata)
    
    if not 'user-id' in request.headers:
        abort(400)
    usernode = request.headers.get('user-id')
    message_id = base64.b64decode(usernode)
    user_id = rsa.decrypt(message_id, priv_key)
    message_user = user_id.decode('utf8')

    if not 'machine-id' in request.headers:
        abort(400)
    machinenode = request.headers.get('machine-id')
    machine_message = base64.b64decode(machinenode)
    machineid = rsa.decrypt(machine_message, priv_key)
    message_machine = machineid.decode('utf8')

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
    print(message_machine)
    print(message_user)
    mach = Machine.query.filter_by(machine_id=message_machine).first()
    if not mach: 
            hist = Machine(owner_id=message_user, machine_id=message_machine)
            db.session.add(hist) 
            db.session.commit()
            mach = Machine.query.filter_by(machine_id=message_machine).first()  
    result = Historic(machine_id = mach.id)
    result.dataos = new_scan
    db.session.add(result) 
    db.session.commit()
    return jsonify({'Scan_added': new_scan}), 201

# Update a parameter passing the id on the route ################################## NOT GOOD
@app.route('/api/scans/<int:scan_id>', methods=['PUT'])
def update_scan(scan_id):
    #scan = [scan for scan in DetectOS if scan['id'] == scan_id]
    scan = Historic.query.filter_by(id=scan_id).first()
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

    scan[0]['machine'] = request.json.get('machine', scan[0]['machine'])
    scan[0]['node'] = request.json.get('node', scan[0]['node'])
    scan[0]['processor'] = request.json.get('processor', scan[0]['processor'])
    scan[0]['release'] = request.json.get('release', scan[0]['release'])
    scan[0]['system'] = request.json.get('system', scan[0]['system'])
    scan[0]['version'] = request.json.get('version', scan[0]['version'])
    return jsonify({'Updated_scan': scan[0]})


@app.route('/api/scans/<int:scan_id>', methods=['DELETE'])
def delete_scan(scan_id):
    scan = Historic.query.filter_by(id=scan_id).first()
    if not scan:
        return jsonify({'message' : 'No machine found!'})
    db.session.delete(scan)
    db.session.commit()
    return jsonify({'result': True})


def make_public_DetectOS(scan):
    new_scan = {}
    for field in scan:
        if field == 'id':
            new_scan['uri'] = url_for('get_scans', scan_id=scan['id'], _external=True)
        else:
            new_scan[field] = scan[field]
    return new_scan
