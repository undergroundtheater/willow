from flask import render_template
#         request, \
#         redirect, \
#         url_for, \
#         flash, \
#         current_app, \
#         session

# from willow.forms import ProfileForm
# from willow.models import Character
from flask.ext.classy import FlaskView
# , route
from flask.ext.security.decorators import login_required
# , roles_required
from flask.ext.security import current_user

class CreateProfileView(FlaskView):
    decorators = [login_required]

class DashboardView(FlaskView):
    base_url="/dashboard"

    @login_required
    def index(self):
#         chars = Character.query.filter(Character.owner == current_user).all()
        return render_template("dashboard.html", characters=list(), owner=current_user)

class CharacterDashboardView(DashboardView):
    pass
