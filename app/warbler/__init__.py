import os
from dotenv import load_dotenv


from flask import Flask, render_template, session, g

from flask_debugtoolbar import DebugToolbarExtension

from .database import (db, connect_db)

from .root.forms import CSRFProtection
from .root.views import root_bp
from .messages.views import messages_bp
from .users.views import users_bp
from .users.userModel import User

#config file
load_dotenv()

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.register_blueprint(root_bp)
app.register_blueprint(messages_bp, url_prefix='/messages')
app.register_blueprint(users_bp, url_prefix='/users')

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
#config file
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ['DATABASE_URL'].replace("postgres://", "postgresql://"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
#config file
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
# toolbar = DebugToolbarExtension(app)

connect_db(app)

if __name__ == "__main__":
    app.run(debug=True)

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

@app.before_request
def generate_CSRF_form():
    """ instantiates CSRF form """

    g.csrf_form = CSRFProtection()

@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""

    return render_template('404.html'), 404

##############################################################################
# Turn off all caching in Flask
#   (useful for dev; in production, this kind of stuff is typically
#   handled elsewhere)
#
# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask

@app.after_request
def add_header(response):
    """Add non-caching headers on every request."""

    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control
    response.cache_control.no_store = True
    return response
