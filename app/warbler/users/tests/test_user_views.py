"""User View tests."""

# run these tests like:
#
#    FLASK_DEBUG=False python -m unittest test_message_views.py


import os
from unittest import TestCase

# from bs4 import BeautifulSoup

from ..userModel import User
from warbler.messages.messageModel import Message
from warbler.follows.followsModel import Follows
from warbler.database import connect_db, db

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

from warbler import app, CURR_USER_KEY
from warbler.root.views import do_logout, do_login, session, g

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

connect_db(app)

db.drop_all()
db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class UserViewTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)
        db.session.flush()

        m1 = Message(text="m1-text", user_id=u1.id)
        db.session.add_all([m1])
        db.session.commit()

        self.u1_id = u1.id
        self.u2_id = u2.id
        self.m1_id = m1.id

        self.client = app.test_client()

    def test_auth_follower_page(self):
            """ Testing that logged in user can access followers page """
            with self.client as c:
                with c.session_transaction() as sess:
                    sess[CURR_USER_KEY] = self.u1_id

                user = User.query.get(self.u1_id)
                user2 = User.query.get(self.u2_id)
                user.followers.append(user2)
                db.session.commit()

                resp = c.get(f"/users/{self.u1_id}/followers")

                html = resp.get_data(as_text=True)

                self.assertEqual(resp.status_code, 200)
                self.assertIn(f"<p>@{ user2.username }</p>", html)

    def test_auth_following_page(self):
        """ Testing that logged in user can access following page """
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

            user = User.query.get(self.u1_id)
            user2 = User.query.get(self.u2_id)
            user.followers.append(user2)
            db.session.commit()

            resp = c.get(f"/users/{ user2.id }/following")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"<p>@{ user.username }</p>", html)

    def test_unauth_access_home(self):
        """ Testing that unlogged in user sees sign up banner """
        with self.client as c:

            resp = c.get("/", follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h4>New to Warbler?</h4>", html)

    def test_auth_access_home(self):
        """ Testing that logged in user sees user page """
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

            user = User.query.get(self.u1_id)

            resp = c.get("/", follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"<p>@{user.username}</p>", html)

    def test_unauth_following_page(self):
        """ Tests that you can't access following page when not logged in """
        with self.client as c:

            resp = c.get(f"/users/{self.u1_id}/following", follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h4>New to Warbler?</h4>", html)

    def test_unauth_followers_page(self):
        """ Tests that you can't access followers page when not logged in """
        with self.client as c:

            resp = c.get(f"/users/{self.u1_id}/followers", follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h4>New to Warbler?</h4>", html)
