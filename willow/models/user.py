from passlib.hash import bcrypt
from flask import current_app, flash, abort
from flask_security.core import current_user
from willow.app import willow_signals, is_admin
from willow.models import db
from flask.ext.security import RoleMixin, UserMixin
from sqlalchemy.ext.declarative import declared_attr

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    active = db.Column(db.Boolean, default=False)
    # flask.ext.security required for production
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

    password_updated = willow_signals.signal('user-updated-password')
    new_user = willow_signals.signal('user-new')
    deletion = willow_signals.signal('user-deletion')
    login_success = willow_signals.signal('user-login-success')
    login_fail = willow_signals.signal('user-login-fail')

    def is_admin(self):
        if hasattr(self, 'wlw_profile'):
            try:
                return self.wlw_profile.is_admin()
            except:
                return False

        return False

    def confirm(self, asofdate=None):
        from datetime import datetime
        from pytz import UTC
        if not asofdate:
            asofdate = datetime.now(UTC)

        self.confirmed_at = asofdate
        if not self.active:
            self.active = True

        db.session.add(self)
        db.session.commit()

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

    def __str__(self):
        return self.name 

    def __repr__(self):
        return u'<Role: %s (%s, %s)>' % (self.name, self.venue, self.chapter)

