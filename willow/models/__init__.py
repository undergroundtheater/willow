from flask.ext.login import LoginManager
from flask.ext.migrate import Migrate
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

from .user import User, Profile
#from .character import Character
from .chapter import Chapter
#from .venue import Venue

# TODO - Create view / template; msk
login_manager.login_view = 'AccountView:login'

@login_manager.user_loader
def load_user(username):
    user = User.query.get(username)
    if not user:
        return None
    user.anonymous = False
    user.authenticated = True
    return user
