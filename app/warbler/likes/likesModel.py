from warbler.database import db


class Like(db.Model):
    """Join table between users and messages (the join represents a like)."""

    __tablename__ = 'likes'

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        primary_key=True,
    )

    message_id = db.Column(
        db.Integer,
        db.ForeignKey('messages.id', ondelete='CASCADE'),
        nullable=False,
        primary_key=True,
    )
