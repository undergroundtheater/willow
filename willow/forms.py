from flask_wtf import Form
from flask_security import forms as secforms
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

class ProfileForm(Form):
    name = StringField('Real Name', validators=[DataRequired()])
