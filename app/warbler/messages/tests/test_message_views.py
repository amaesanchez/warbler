"""Message View tests."""

# run these tests like:
#
#    FLASK_DEBUG=False python -m unittest test_message_views.py


import os
from unittest import TestCase

from warbler.database import db, connect_db
from warbler.messages.messageModel import Message
from warbler.users.userModel import User

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

from warbler import app, CURR_USER_KEY

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

connect_db(app)

db.drop_all()
db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class MessageBaseViewTestCase(TestCase):
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

    def tearDown(self):
        """ Rolls back the test environment and actions made in tests """
        db.session.rollback()


class MessageAddViewTestCase(MessageBaseViewTestCase):
    def test_add_message(self):
        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

            # Now, that session setting is saved, so we can have
            # the rest of ours test
            resp = c.post("/messages/new", data={"text": "Hello"})

            self.assertEqual(resp.status_code, 302)

            Message.query.filter_by(text="Hello").one()

    def test_unauth_add_msg(self):
        """ Testing that unlogged in user cant add message """
        with self.client as c:

            resp = c.post("/messages/new", data={
                "text" : "random"
            }, follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized.", html)

    def test_unauth_view_add_form(self):
        """ Testing that unlogged user cannot see add msg form """

        with self.client as c:

            resp = c.get("/messages/new", follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized.", html)

    def test_unauth_delete_msg(self):
        """ Testing that unlogged in user cant add message """
        with self.client as c:

            resp = c.post(f"/messages/{self.m1_id}/delete",
                            follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized.", html)

    def test_auth_view_add_msg(self):
        """ Testing that logged in user can see add msg form """
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

            resp = c.get("/messages/new", follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Add my message!</button>", html)

    def test_auth_add_msg(self):
        """ Testing that logged in user can add message """
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

            resp = c.post("/messages/new", data={
                "text" : "random"
            }, follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("random", html)

    def test_auth_delete_msg(self):
        """ Testing that logged in user can delete a message """

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

            message = Message.query.get(self.m1_id)

            resp = c.post(f"/messages/{self.m1_id}/delete",
                            follow_redirects=True)

            html = resp.get_data(as_text=True)

            deleted_message = Message.query.get(self.m1_id)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p class="small">Messages</p>', html)
            self.assertNotIn(message.text, html)
            self.assertIsNone(deleted_message)

    def test_auth_other_dmsg_delete(self):
        """ Testing that logged in user can't delete other user's message """

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u2_id

            resp = c.post(f"/messages/{self.m1_id}/delete",
                            follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized.", html)
