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
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from willow.models import User, Chapter, Venue

from flask import current_app
from werkzeug.utils import import_string

def get_chapter_query():
    return Chapter.query

def get_chapter_name(instance):
    return "%s (%s)" % (instance.name, instance.venue.name)

def get_venue_query():
    return Venue.query

class WLWForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[])
    
class ProfileForm(Form):
    name = StringField('Real Name', validators=[DataRequired()])
    primary_chapter = QuerySelectField("Primary Chapter",
            query_factory=get_chapter_query,
            get_label=get_chapter_name,
            allow_blank=True,
            blank_text=u'Unassociated')

class NewCharacterForm(WLWForm):
    private_description = TextAreaField('Private Description', validators=[])
    chapter = QuerySelectField("Chapter",
            query_factory=get_chapter_query,
            get_label=get_chapter_name)

class NewChapterForm(WLWForm):
    venue = QuerySelectField("Venue",
            query_factory=get_venue_query,
            get_label='name')

class NewVenueForm(WLWForm):
    pass

class AdminUserForm(WLWForm):
    pass

class NewRoleForm(WLWForm):
    chapter = QuerySelectField("Chapter",
            query_factory=get_chapter_query,
            get_label=get_chapter_name,
            allow_blank=True,
            blank_text=u'Unassociated')
    venue = QuerySelectField("Venue",
            query_factory=get_venue_query,
            get_label='name',
            allow_blank=True,
            blank_text=u'Unassociated')
