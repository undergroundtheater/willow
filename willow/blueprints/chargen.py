from flask import render_template, \
        redirect, \
        url_for, \
        flash, \
        current_app, \
        session

from flask.ext.classy import FlaskView, route
from werkzeug.utils import import_string

from willow.models import db, Character
from willow.forms import NewCharacterForm

class ChargenView(FlaskView):
    """
    This should be sub-classed by plugins.  Custom views should
    be added to settings.py for example:

    CHARGEN_VIEW = 'pluginmodule.chargen.GenericChargenView'
    """

    route_base = '/chargen'

    steps = [ 'basics' ]

    character_form = NewCharacterForm

    # TODO - add flash message notifications for steps

    @route('/')
    @route('/new')
    def index(self):
        session['chargen_index'] = 0
        form = self.character_form()
        return render_template('chargen/index.html', form=form)

    def before_post(self, *args, **kwargs):
        si = int(session['chargen_index'])
        self.step_name = self.steps[si]
        self.step_data = kwargs

        si += 1
        if si > len(self.steps):
            si = -1

        self.next_step = si

    def post(self, character_id=None):
        self.character_id = character_id
        character = self._process_step()
        return render_template('chargen/step.html',
                character=character,
                next_step=self.next_step,
                step_info=self.step_data[self.step_name],
                )

    def _process_step(self, **kwargs):
        methodname = "_chargen_%s" % (self.step_name,)
        method = getattr(self, methodname)
        return method(**kwargs)

    def _chargen_basics(self, **kwargs):
        self.form = NewCharacterForm()

        if self.character_id is not None:
            # Updating on confirmation page
            character = Character.query.get(self.character_id)
        else:
            character = Character()

        if self.form.validate_on_submit():
            self.form.populate_obj(character)

        character.active = True

        db.session.add(character)
        db.session.commit()

        return character
