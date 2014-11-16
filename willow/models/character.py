from flask import current_app, flash, abort
from willow.app import willow_signals
from willow.models import db, mixins
from flask.ext.security import RoleMixin, UserMixin

class Character(db.Model, mixins.WLWMixin):
    private_description = db.Column(db.Text, nullable=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    chapter = db.relationship('Chapter',
            primaryjoin="Character.chapter_id == Chapter.id",
            uselist=False,
            cascade=False,
            backref=db.backref('characters', uselist=True))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    owner = db.relationship('User',
            primaryjoin="Character.owner_id == User.id",
            # TODO - re-evaluate for multi-owner characters; for example, NPCs.
            uselist=False,
            cascade=False,
            backref=db.backref('characters', uselist=True))
