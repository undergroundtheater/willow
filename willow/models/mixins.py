from flask import current_app, flash, abort
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import event
from flask.ext.login import current_user
from willow.app import willow_signals
from willow.models import db

class WLWMixin(object):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    expired = db.Column(db.Boolean, default=False)
    hidden = db.Column(db.Boolean, default=False)
    admin = db.Column(db.Boolean, default=False)
    created_on = db.Column(db.DateTime(timezone=True),
            default=db.func.now())
    updated_on = db.Column(db.DateTime(timezone=True),
            default=db.func.now(),
            onupdate=db.func.now())

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def is_expired(self):
        return self.expired

    def is_hidden(self):
        return self.hidden

    def is_admin(self):
        return self.admin

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, str(self))
