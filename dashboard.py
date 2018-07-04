from views import *
from app import app
import requests
from forms import DeleteMachineForm
from model import *

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
