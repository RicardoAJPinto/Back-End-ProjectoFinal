# Flask-dance
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin, SQLAlchemyBackend
from flask_login import UserMixin, current_user, LoginManager, login_required, login_user, logout_user
from flask_dance.consumer import oauth_authorized
from app import *

login_manager = LoginManager(app)

# Flask dance section
twitter_blueprint = make_twitter_blueprint(
    api_key='qfuG0YBH6qWWBZB6QsqbWs6lE',
    api_secret='ZD96F3K2GVapUE3VqSacKehKeSaY9E8xUHNTpHswNlQNjVM5ww',
)

github_blueprint = make_github_blueprint(
    client_id='647e0785c17a789e69cd',
    client_secret='8e8f75bbfec49a65dfb027ee58b521f1fe432903',
)

app.register_blueprint(twitter_blueprint, url_prefix='/twitter_login')
app.register_blueprint(github_blueprint, url_prefix='/github_login')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from model import *
# Connection to regist on DB
#twitter_blueprint.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)
#github_blueprint.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)


@app.route('/dance')
@login_required
def dance():
    return '<h1> You are logged in as {} </h1>'.format(current_user.username)

@app.route('/adios')
@login_required
def logout():
    logout_user()
    return redirect(url_for('dance'))

@app.route('/twitter')
def twitter_login():
    if not twitter.authorized:
        return redirect(url_for('twitter.login'))

    account_info = twitter.get('/account/setting.json')

    if account_info.ok:
        account_info_json = account_info.json()

        return '<h1>Your twitter name is @{}'.format(account_info_json['screen_name'])
        
    return '<h1> Request failed </h1>'

# Signal
@oauth_authorized.connect_via(twitter_blueprint)
def twitter_logged_in(blueprint, token):
    account_info = blueprint.session.get('/account/setting.json')

    if account_info.ok:
        account_info_json = account_info.json()
        username = account_info_json['screen_name']



@app.route('/github')
def github_login():
    if not github.authorized:
        return redirect(url_for('github.login'))

    account_info = github.get('/user')

    if account_info.ok:
        account_info_json = account_info.json()

        return '<h1>Your github name is {}'.format(account_info_json['login'])
        
    return '<h1> Request failed </h1>'