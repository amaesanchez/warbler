from flask import Blueprint, render_template, flash, redirect, g, request
from .userEditForm import UserEditForm, ChangePasswordForm
from warbler.database import db
from .userModel import User, DEFAULT_HEADER_IMAGE_URL, DEFAULT_IMAGE_URL
from ..messages.messageModel import Message
from ..root.views import do_logout

users_bp = Blueprint('users_bp', __name__,
    template_folder='templates',
    static_folder='static')

##############################################################################
# General user routes:

@users_bp.get('/')
def list_users():
    """Page with listing of users.

    Can take a 'q' param in querystring to search by that username.
    """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    search = request.args.get('q')

    if not search:
        users = User.query.all()
    else:
        users = User.query.filter(User.username.like(f"%{search}%")).all()

    return render_template('index.html', users=users)


@users_bp.get('/<int:user_id>')
def show_user(user_id):
    """Show user profile."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)

    return render_template('show.html', user=user)


@users_bp.get('/<int:user_id>/following')
def show_following(user_id):
    """Show list of people this user is following."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)
    return render_template('following.html', user=user)


@users_bp.get('/<int:user_id>/followers')
def show_followers(user_id):
    """Show list of followers of this user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)
    return render_template('followers.html', user=user)


@users_bp.post('/follow/<int:follow_id>')
def start_following(follow_id):
    """Add a follow for the currently-logged-in user.

    Redirect to following page for the current for the current user.
    """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    followed_user = User.query.get_or_404(follow_id)
    g.user.following.append(followed_user)
    db.session.commit()

    return redirect(f"/users/{g.user.id}/following")


@users_bp.post('/stop-following/<int:follow_id>')
def stop_following(follow_id):
    """Have currently-logged-in-user stop following this user.

    Redirect to following page for the current for the current user.
    """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    followed_user = User.query.get(follow_id)
    g.user.following.remove(followed_user)
    db.session.commit()

    return redirect(f"/users/{g.user.id}/following")


@users_bp.route('/profile', methods=["GET", "POST"])
def profile():
    """Update profile for current user."""

    if not g.user:
        return redirect("/")

    form = UserEditForm(obj=g.user)

    if form.validate_on_submit():
        g.user.username = form.username.data
        g.user.email = form.email.data
        g.user.image_url = form.image_url.data or DEFAULT_IMAGE_URL
        g.user.header_image_url = form.header_image_url.data or DEFAULT_HEADER_IMAGE_URL
        g.user.bio = form.bio.data

        if not User.authenticate(g.user.username, form.data.get("password")):
            form.password.errors = ["Incorrect password"]
        else:
            db.session.commit()
            return redirect(f"/users/{g.user.id}")

    return render_template("edit.html", form=form)

@users_bp.route('/changepwd', methods=["GET", "POST"])
def change_pwd():
    """Change the password for current user."""

    if not g.user:
        return redirect("/")

    form = ChangePasswordForm(obj=g.user)

    if form.validate_on_submit():

        if not User.authenticate(g.user.username, form.data.get("password")):
            form.password.errors = ["Incorrect password"]
        else:
            password1 = form.New_password1.data
            password2 = form.New_password2.data
            if not password1 == password2:
                form.New_password2.errors = ["New passwords do not match."]

            else:
                g.user.password = User.hash_password(password1)
                db.session.commit()

                return redirect(f"/users/{g.user.id}")

    return render_template("edit.html", form=form)

@users_bp.get('/<int:user_id>/likes')
def likes_page(user_id):
    """ Shows a page that displays all liked messages by user """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    if not user_id == g.user.id:
        user = User.query.get_or_404(user_id)
        liked_messages = [Message.query.get(like.id) for like in user.messages_liked]
    else:
        user = g.user
        liked_messages = [Message.query.get(like.id) for like in g.user.messages_liked]

    return render_template('liked-messages.html', messages = liked_messages, user=user)

@users_bp.post('/delete')
def delete_user():
    """Delete user.

    Redirect to signup page.
    """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    Message.query.filter_by(user_id=g.user.id).delete()
    User.query.filter_by(id=g.user.id).delete()

    db.session.commit()

    flash(f"Account successfully deleted.", "success")

    return redirect("/signup")
