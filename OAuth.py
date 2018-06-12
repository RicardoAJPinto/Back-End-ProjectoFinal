# Flask-dance
from flask import Flask, redirect, url_for, flash, render_template
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin, SQLAlchemyBackend
from flask_login import UserMixin, current_user, LoginManager, login_required, login_user, logout_user
from flask_dance.consumer import oauth_authorized, oauth_error
from sqlalchemy.orm.exc import NoResultFound
from app import *
import sys

github_blueprint = make_github_blueprint(
    client_id='647e0785c17a789e69cd',
    client_secret='8e8f75bbfec49a65dfb027ee58b521f1fe432903',
)

app.register_blueprint(github_blueprint, url_prefix='/github_login')

from model import *

login_manager = LoginManager()
login_manager.login_view = 'github.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Connection to regist on DB
github_blueprint.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)


@oauth_authorized.connect_via(github_blueprint)
def github_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in with GitHub.", category="error")
        return False
    
    resp = blueprint.session.get("/user")

    if not resp.ok:
        msg = "Failed to fetch user info from GitHub."
        flash(msg, category="error")
        return False     

    github_info = resp.json()
    github_user_id = str(github_info["id"])

    # Find this OAuth token in the database, or create it
    query = OAuth.query.filter_by(
        provider=blueprint.name,
        id=github_user_id,
    )
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(
            provider=blueprint.name,
            id=github_user_id,
            token=token,
        )

    if oauth.user:
        login_user(oauth.user)
        flash("Successfully signed in with GitHub.")

    else:
        # Create a new local user account for this user
        user = User(
            # Remember that `email` can be None, if the user declines
            # to publish their email address on GitHub!
            email=github_info["email"],
            #name=github_info["name"],
        )
        # Associate the new local user account with the OAuth token
        oauth.user = user
        # Save and commit our database models
        db.session.add_all([user, oauth])
        db.session.commit()
        # Log in the new local user account
        login_user(user)
        flash("Successfully signed in with GitHub.")

    # Disable Flask-Dance's default behavior for saving the OAuth token
    return False