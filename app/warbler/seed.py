"""Seed database with sample data from CSV Files."""

from csv import DictReader
from warbler.database import db
from .follows.followsModel import Follows
from .messages.messageModel import Message
from .users.userModel import User

db.drop_all()
db.create_all()

with open('generator/users.csv') as users:
    db.session.bulk_insert_mappings(User, DictReader(users))

with open('generator/messages.csv') as messages:
    db.session.bulk_insert_mappings(Message, DictReader(messages))

with open('generator/follows.csv') as follows:
    db.session.bulk_insert_mappings(Follows, DictReader(follows))

db.session.commit()
