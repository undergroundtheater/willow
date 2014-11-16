# from flask import current_app, flash, abort
# from willow.app import willow_signals
from willow.models import db, mixins

class Chapter(db.Model, mixins.WLWMixin):
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    venue = db.relationship('Venue',
            primaryjoin="Chapter.venue_id == Venue.id",
            uselist=False,
            cascade=False,
            backref=db.backref('chapters', uselist=True, cascade="all, delete-orphan"))