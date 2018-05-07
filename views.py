from app import app
from model import *
##############################################################################
# Views
##############################################################################
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/forgotpass')
def forgot():
    return render_template('security/forgot_password.html')

@app.route('/add')
def add():
    return render_template('add_user.html')

@app.route('/delete', methods=['POST'])
@login_required
def delete():
    userdel = User.query.filter_by(id=request.form['id']).first()
    db.session.delete(userdel)
    db.session.commit()
    user = User.query.all()
    return render_template('show.html', user=user)

@app.route('/show')
@login_required
def show():
    user = User.query.all() 
    return render_template('show.html', user=user)
    
@app.route('/profile/<email>')
@login_required
def profile(email):
    user = User.query.filter_by(email=email).first()
    return render_template('profile.html',  user=user)

@app.route('/post_user', methods=['POST'])
def post_user():
    user = User(email=request.form['email'], password=request.form['password'])
    db.session.add(user) #add object
    db.session.commit()  #save 
    return redirect(url_for('index'))

#Configuration of JWT
@app.route('/token/auth', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = User.query.all()
    for user in user: 
        if user.email == email and user.password == password:
            access_token = create_access_token(identity=user.email)
            refresh_token = create_refresh_token(identity=user.email)
            # Set the JWTs and the CSRF double submit protection cookies
            # in this response
            resp = jsonify({'login': True})
            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)
            return resp, 200
                      
    return jsonify({'login': False}), 401  
    
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    ret = {
        'current_identity': get_jwt_identity(),  # test
    }
    return jsonify(ret), 200

@app.route('/token/remove', methods=['POST'])
def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200