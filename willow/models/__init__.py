from flask.ext.login import LoginManager
from flask.ext.migrate import Migrate
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

from .user import User
#from .character import Character
from .chapter import Chapter
#from .venue import Venue

# TODO - Create view / template; msk
login_manager.login_view = 'AccountView:login'

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return None
    user.anonymous = False
    user.authenticated = True
    return user
