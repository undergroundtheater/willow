from flask.ext.classy import FlaskView, route
from flask_security.decorators import login_required
from .chargen import ChargenView
from .admin import admin_blueprint
from .chargen import chargen_blueprint
