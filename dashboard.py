from views import *

@app.route('/quickstart')
@login_required
def quickstart():
    return render_template('dashboard/quickstart.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard/Inspirationexample.html')
