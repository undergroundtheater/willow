from passlib.hash import bcrypt
from flask import current_app, flash, abort
from flask.ext.login import current_user
from willow.app import willow_signals
from willow.models import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    profile_id = db.Column(db.Integer, nullable=True)
    last_ip = db.Column(db.String, default='127.0.0.1')
    last_login_on = db.Column(db.DateTime, default=db.func.now())
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now())
    anonymous = True
    authenticated = False

    profile = db.relationship('Profile', primaryjoin='foreign(User.profile_id) == Profile.id', uselist=False, cascade=False, lazy='joined')

    def update_password(self, new_password):
        self.password = bcrypt.encrypt(new_password)

    def check_password(self, password):
        return bcrypt.verify(password, self.password)

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return self.profile.is_active()

    def is_anonymous(self):
        return self.anonymous

    password_updated = willow_signals.signal('user-updated-password')
    new_user = willow_signals.signal('user-new')
    deletion = willow_signals.signal('user-deletion')
    login_success = willow_signals.signal('user-login-success')
    login_fail = willow_signals.signal('user-login-fail')


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    active = db.Column(db.Boolean, default=False)
    admin = db.Column(db.Boolean, default=False)
    primary_chapter_id = db.Column(db.Integer, nullable=True)
    primary_chapter = db.relationship('Chapter', primaryjoin='foreign(Profile.primary_chapter_id) == Chapter.id', uselist=False, cascade=False, lazy='joined')

    def is_active(self):
        return self.active

    def is_admin(self):
        return self.admin
