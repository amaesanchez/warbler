"""User View tests."""

# run these tests like:
#
#    FLASK_DEBUG=False python -m unittest test_message_views.py


import os
from unittest import TestCase

# from bs4 import BeautifulSoup

from warbler.database import db, connect_db
from warbler.users.userModel import User

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

from warbler import app, CURR_USER_KEY

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

db.drop_all()
db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class HomeViewTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)

        db.session.add_all([u1])
        db.session.commit()

        self.u1_id = u1.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_home_logged_in(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id
            resp = c.get(
                "/",
                follow_redirects=True,)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("@u1", html)
            self.assertIn("Log out", html)

    def test_home_logged_out(self):
        with self.client as c:

            resp = c.get(
                "/",
                follow_redirects=True,)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Sign up", html)
            self.assertIn("Log in", html)
            self.assertIn("Happening?", html)
