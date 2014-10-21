from passlib.hash import bcrypt
from flask import current_app, flash, abort
from flask.ext.login import current_user
from willow.app import willow_signals
from willow.models import db
from flask.ext.security import RoleMixin, UserMixin

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))
        

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    active = db.Column(db.Boolean, default=False)
    # flask.ext.security required
    confirmed_at = db.Column(db.DateTime)
    # end flask.ext.security
    created_on = db.Column(db.DateTime(timezone=True),
            default=db.func.now())
    updated_on = db.Column(db.DateTime(timezone=True),
            default=db.func.now(),
            onupdate=db.func.now())
    roles = db.relationship('Role', secondary=roles_users,
            backref=db.backref('users', lazy='dynamic'))
    anonymous = True
    authenticated = False

    def update_password(self, new_password):
        self.password = bcrypt.encrypt(new_password)

    def check_password(self, password):
        return bcrypt.verify(password, self.password)

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return self.active

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
    user = db.relationship('User',
            primaryjoin='foreign(Profile.user_id) == User.id',
            uselist=False,
            cascade=False,
            lazy='joined',
            backref=db.backref('profile', uselist=False, lazy='joined'))

    admin = db.Column(db.Boolean, default=False)
    primary_chapter_id = db.Column(db.Integer, nullable=True)
    primary_chapter = db.relationship('Chapter', primaryjoin='foreign(Profile.primary_chapter_id) == Chapter.id', uselist=False, cascade=False, lazy='joined')

    def is_active(self):
        return self.user.is_active()

    def is_admin(self):
        return self.admin

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=True)
    chapter = db.relationship('Chapter',
            primaryjoin='foreign(Role.chapter_id) == Chapter.id',
            uselist=False,
            cascade=False,
            backref=db.backref('roles', uselist=True, order_by=id)
            )
    venue = db.relationship('Venue',
            primaryjoin='foreign(Role.venue_id) == Venue.id',
            uselist=False, 
            cascade=False,
            backref=db.backref('roles', uselist=True, order_by=id)
            )
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now())

    def __eq__(self, other):
        return (
                (self.name == other.name and self.chapter == other.chapter) or
                (self.name == getattr(other, 'name', None) and self.chapter == getattr(other, 'chapter', None))
                )

