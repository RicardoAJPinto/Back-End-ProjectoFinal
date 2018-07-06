from views import *
################################ Reset Password #################################
@app.route('/reset_password', methods=['GET', 'POST'])
def resetpwd():
    form = RequestResetForm()
    return render_template('resetpassword.html', form=form)


# Reset password (POSTTTTTT)
@app.route('/reseted', methods=['POST'])
def reseted():
    email = request.form.get('email')
    try:
        user = User.query.filter_by(email=email).first()
    except:
        return render_template('resetpassword.html', form=email)
         
    if user:
        s = URLSafeTimedSerializer('Thisisasecret!')
        token = s.dumps(user.email, salt='email-confirm')
        msg = Message('Confirm Email', sender='ZeusNoReply@gmail.com', recipients=[user.email])
        link = url_for('reset_with_token', token=token, _external=True)
        msg.body = 'Your link to new password is {}'.format(link)
        mail.send(msg)
        
    return render_template('resetpassword.html', form=RequestResetForm(), message=flash('You have received an email to reset your password!', 'success'))
 

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
        return render_template('404.html')
 
    return render_template('newpassword.html', form=form, token=token, message=flash('Your password has been updated!', 'success'))

# After the email has been sended
@app.route('/new_password/<token>', methods=['GET', 'POST'])
def newpwd(token):
    form = ResetPasswordForm()
    return render_template('newpassword.html', form=form)
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.passowrd.data)
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! Now you are able to log in')
        return redirect(url_for('login'))

