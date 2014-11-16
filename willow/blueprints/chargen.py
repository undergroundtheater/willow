from flask import render_template, \
        redirect, \
        Blueprint, \
        flash, \
        current_app, \
        session, \
        url_for

from flask.ext.classy import FlaskView, route
from flask.ext.security import current_user
from werkzeug.utils import import_string

from willow.models import db, Character
from willow.forms import NewCharacterForm

chargen_blueprint = Blueprint('chargen', __name__)

class ChargenView(FlaskView):
    """
    This should be sub-classed by plugins.  Custom views should
    be added to settings.py for example:

    CHARGEN_VIEW = 'pluginmodule.chargen.GenericChargenView'
    """

    route_base = '/'

    # TODO - add flash message notifications for steps

    @route('/', methods=['GET', 'POST'])
    def index(self):
        form = NewCharacterForm()
        if form.validate_on_submit():
            character = Character()
            form.populate_obj(character)

            character.owner = current_user

            character.active = True
            db.session.add(character)
            db.session.commit()

            return render_template('chargen/done.html', character=character)

        return render_template('chargen/index.html', form=form)

    @route('<pkid>/update', methods=['POST'])
    def update(self):
        return redirect('/dashboard')

ChargenView.register(chargen_blueprint)
