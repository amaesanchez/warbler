from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class UserEditForm(FlaskForm):
    """Form for editing users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    image_url = StringField('(Optional) Image URL')
    header_image_url = StringField('(Optional) Header Image URL')
    bio = TextAreaField('(Optional) Tell us about yourself')
    password = PasswordField('Password', validators=[Length(min=6)])
    


class ChangePasswordForm(FlaskForm):
    """ Edit a user's info form """

    New_password1 = PasswordField('New Password', validators=[Length(min=6)])
    New_password2 = PasswordField('Confirm New Password', validators=[Length(min=6)])
    password = PasswordField('Password', validators=[Length(min=6)])
