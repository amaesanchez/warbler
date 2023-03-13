from flask import Blueprint, render_template, flash, redirect, session, g
from .forms import (UserAddForm, LoginForm)
from warbler.database import db
from sqlalchemy.exc import IntegrityError
from ..users.userModel import User
from ..messages.messageModel import Message

root_bp = Blueprint('root_bp', __name__,
    template_folder='templates',
    static_folder='static')

CURR_USER_KEY = "curr_user"


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Log out user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@root_bp.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('signup.html', form=form)


@root_bp.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login and redirect to homepage on success."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(
            form.username.data,
            form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)


@root_bp.post('/logout')
def logout():
    """Handle logout of user and redirect to homepage."""


    # IMPLEMENT THIS AND FIX BUG
    # DO NOT CHANGE METHOD ON ROUTE

    if g.csrf_form.validate_on_submit() and g.user:
        do_logout()

    return redirect('/')


##############################################################################
# Homepage and error pages


@root_bp.get('/')
def homepage():
    """Show homepage:

    - anon users: no messages
    - logged in: 100 most recent messages of followed_users
    """

    if g.user:
        followers_ids = [user.id for user in g.user.following] + [g.user.id]
        # all_messages = Message.query.all()
        # list_of_messages = [ msg for msg in all_messages
        #     if msg.user_id in g.user.followers
        #     or msg.user_id == g.user.id]

        messages = (Message
                    .query
                    .filter(Message.user_id.in_(followers_ids))
                    .order_by(Message.timestamp.desc())
                    .limit(100)
                    .all()
                    )

        return render_template('home.html', messages=messages)

    else:
        return render_template('home-anon.html')
