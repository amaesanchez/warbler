"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError

from ..userModel import User
from warbler.database import connect_db, db

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

from warbler import app

connect_db(app)

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    def setUp(self):
        """ sets up the test environment """
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

        self.client = app.test_client()

    def tearDown(self):
        """ Rolls back the test environment and actions made in tests """
        db.session.rollback()

    def test_user_model(self):
        """ Tests that the user has no messages/followers """

        u1 = User.query.get(self.u1_id)

        # User should have no messages & no followers
        self.assertEqual(len(u1.messages), 0)
        self.assertEqual(len(u1.followers), 0)

    def test_is_following(self):
        """ Tests that u1 is following u2 and modifying the Follows table """

        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        u1.following.append(u2)
        db.session.commit()

        self.assertTrue(u1.is_following(u2))

    def test_is_not_following(self):
        """ Tests that u1 is not following u2 """

        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        self.assertFalse(u1.is_following(u2))

    def test_is_followed_by(self):
        """ Tests that u2 is following u1 and modifying the Follows table """

        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        u1.followers.append(u2)
        db.session.commit()

        self.assertTrue(u1.is_followed_by(u2))

    def test_u2_is_not_following(self):
        """ Tests that u2 is not following u1 """

        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        self.assertFalse(u1.is_followed_by(u2))

    def test_create_new_user(self):
        """ Tests that a new user is created on signup """

        user = User.signup(username="new_user", email="new@gmail.com",
            password="newpassword")

        db.session.add(user)
        db.session.commit()

        self.assertIsInstance(User.query.get(user.id), User)

    def test_signup_duplicate(self):
        """ Tests that an error will be thrown when a duplicate user is created"""

        user = User.signup(username="new_user", email="new@gmail.com",
            password="newpassword")

        user2 = User.signup(username="new_user", email="new@gmail.com",
            password="newpassword")

        db.session.add_all([user, user2])

        self.assertRaises(IntegrityError, db.session.commit)

    def test_user_auth(self):
        """ Tests that the authenticate User class method works as expected """
        u1 = User.query.get(self.u1_id)
        auth = User.authenticate(u1.username, 'password')

        self.assertIsInstance(auth, User)

    def test_user_fail_pw_auth(self):
        """ Tests that the authenticate User class method doesn't works with incorrect password """
        u1 = User.query.get(self.u1_id)
        auth = User.authenticate(u1.username, 'taco')

        self.assertNotIsInstance(auth, User)

    def test_user_fail_un_auth(self):
        """ Tests that the authenticate User class method doesn't works with incorrect username """
        auth = User.authenticate('username', 'password')

        self.assertNotIsInstance(auth, User)
