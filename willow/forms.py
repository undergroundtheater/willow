from flask_wtf import Form
from wtforms import IntegerField, \
        StringField, \
        PasswordField,\
        ValidationError, \
        SelectField, \
        TextAreaField, \
        BooleanField, \
        HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from willow.models import User, Profile

def email_check():
    def _email(form, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("{} is already being used.".format(field.data))
    return _email

class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class NewUserForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(), email_check()])
    password = PasswordField('Password', validators=[DataRequired(),
        EqualTo('confirm', message='Passwords must match.')])
    confirm = PasswordField('Confirm')

class ProfileForm(Form):
    name = StringField('Real Name', validators=[DataRequired()])
