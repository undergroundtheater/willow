from flask import render_template, \
        request, \
        redirect, \
        url_for, \
        flash, \
        current_app, \
        session

from willow.forms import ProfileForm
from willow.models import Character
from flask.ext.classy import FlaskView, route
from flask.ext.security.decorators import login_required, roles_required
from flask.ext.security import current_user

class DashboardView(FlaskView):
    base_url="/dashboard"

    @login_required
    def index(self):
        chars = Character.query.filter(Character.owner == current_user).all()
        return render_template("dashboard.html", characters=chars, owner=current_user)

class CharacterDashboardView(DashboardView):
    pass

class WLWView(FlaskView):
    decorators = [login_required]
    route_base='/'
    redirect_view = None
    default_template = "willow/index.html"

    @route('/')
    @route('/dashboard')
    def index(self):
        return render_template(self.get_template())

    def get_template(self,action=None):
        if action is None:
            return self.default_template
        return "%s_%s.html" % (self.route_base, action)

    def get_blueprint(self):
        if hasattr(request, 'blueprint'):
            return request.blueprint
        else:
            return None
