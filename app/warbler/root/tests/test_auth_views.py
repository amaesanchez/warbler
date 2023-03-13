"""Auth View tests."""

# run these tests like:
#
#    FLASK_DEBUG=False python -m unittest test_message_views.py

import os
from unittest import TestCase

from warbler.database import db
from warbler.messages.messageModel import Message
from warbler.users.userModel import User

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

from warbler import app, CURR_USER_KEY

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['WTF_CSRF_ENABLED'] = False

db.drop_all()
db.create_all()

class AuthViewTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        db.session.flush()

        m1 = Message(text="m1-text", user_id=u1.id)
        db.session.add_all([m1])
        db.session.commit()

        self.u1_id = u1.id
        self.m1_id = m1.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_signup_success(self):
        with self.client as c:
            resp = c.post(
                "/signup",
                data={
                    "username": "newU",
                    "password": "password",
                    "email": "newEmail@email.com",
                    "image_url": None
                },
                follow_redirects=True,)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("@newU", html)

    def test_signup_dupe_username(self):
        with self.client as c:
            resp = c.post(
                "/signup",
                data={
                    "username": "u1",
                    "password": "password",
                    "email": "newEmail@email.com",
                    "image_url": None
                },
                follow_redirects=True,)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Username already taken", html)

    def test_signup_dupe_email(self):
        with self.client as c:
            resp = c.post(
                "/signup",
                data={
                    "username": "newU",
                    "password": "password",
                    "email": "u1@email.com",
                    "image_url": None
                },
                follow_redirects=True,)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Username already taken", html)

    def test_login(self):
        with self.client as c:
            resp = c.post(
                "/login",
                data={
                    "username": "u1",
                    "password": "password",
                },
                follow_redirects=True,)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Hello, u1!", html)
            self.assertIn("@u1", html)

    def test_login_wrong_password(self):
        with self.client as c:
            resp = c.post(
                "/login",
                data={
                    "username": "u1",
                    "password": "badpassword",
                },
                follow_redirects=True,)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Invalid credentials.", html)
            self.assertIn("Welcome back.", html)

    def test_login_wrong_password_username(self):
        with self.client as c:
            resp = c.post(
                "/login",
                data={
                    "username": "badu1",
                    "password": "badpassword",
                },
                follow_redirects=True,)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Invalid credentials.", html)
            self.assertIn("Welcome back.", html)

    def test_logout(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

            resp = c.post(
                "/logout",
                follow_redirects=True,)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Welcome back.", html)

    def test_logout_no_authentication(self):
        with self.client as c:

            resp = c.post(
                "/logout",
                follow_redirects=True,)

            html = resp.get_data(as_text=True)

            self.assertIn("Access unauthorized.", html)
            self.assertIn("Happening?", html)
