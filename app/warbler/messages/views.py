from flask import Blueprint, render_template, flash, redirect, g, jsonify, abort
from .messageForm import MessageForm
from .messageModel import Message
from ..likes.likesModel import Like
from warbler.database import db

messages_bp = Blueprint('messages_bp', __name__,
    template_folder='templates',
    static_folder='static')

##############################################################################
# Messages routes:

@messages_bp.route('/new', methods=["GET", "POST"])
def add_message():
    """Add a message:

    Show form if GET. If valid, update message and redirect to user page.
    """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = MessageForm()

    if form.validate_on_submit():
        msg = Message(text=form.text.data)
        g.user.messages.append(msg)
        db.session.commit()

        return redirect(f"/users/{g.user.id}")

    return render_template('create.html', form=form)


@messages_bp.get('/<int:message_id>')
def show_message(message_id):
    """Show a message."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    msg = Message.query.get_or_404(message_id)
    return render_template('show-msg.html', message=msg)


@messages_bp.post('/<int:message_id>/delete')
def delete_message(message_id):
    """Delete a message.

    Checks if this message was written by the current user.
    Redirect to user page on success.
    """
    msg = Message.query.get_or_404(message_id)

    if not g.user or not msg.user_id == g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    db.session.delete(msg)
    db.session.commit()

    return redirect(f"/users/{g.user.id}")

@messages_bp.post('/<int:message_id>/like')
def like_message(message_id):
    """ adds message to likes of a user """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    message = Message.query.get_or_404(message_id)

    if message in g.user.liked_messages:
        g.user.liked_messages.remove(message)
    else:
        g.user.liked_messages.append(message)

    db.session.commit()

    return jsonify(messageID = message_id)
