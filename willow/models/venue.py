from flask import current_app, flash, abort
from willow.app import willow_signals
from slugify import slugify
from willow.models import db, mixins

class Venue(db.Model, mixins.WLWMixin):
    pass
