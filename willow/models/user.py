from passlib.hash import bcrypt
from flask import current_app, flash, abort
from flask.ext.login import current_user
from willow.app import willow_signals
from willow.models import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    active = db.Column(db.Boolean, default=False)
    last_ip = db.Column(db.String, default='127.0.0.1')
    last_login_on = db.Column(db.DateTime, default=db.func.now())
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now())
    primary_chapter_id = db.Column(db.Integer, nullable=True)
    anonymous = True
    authenticated = False

    primary_chapter = db.relationship('Chapter', primaryjoin='foreign(User.primary_chapter_id) == Chapter.id', uselist=False, cascade=False, lazy='dynamic')
