from views import *
import requests

@app.route('/quickstart')
@login_required
def quickstart():
    return render_template('dashboard/quickstart.html')

@app.route('/dashboard')
@login_required
def dashboard():
    url = 'http://127.0.0.1:5000/api/scans'
    insertAPIkey = str(current_user.api_key)
    headers= { "x-api-key": insertAPIkey} 

    requestpost = requests.get(url , headers=headers).json()
    print(requestpost)
    json_size = len(requestpost["DetectOS"])
    print(json_size)
    return render_template('dashboard/Inspirationexample.html', APIcall=requestpost, json_size=json_size)
