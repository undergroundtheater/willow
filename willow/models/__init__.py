from flask.ext.migrate import Migrate
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import SQLAlchemyUserDatastore, Security

db = SQLAlchemy()
migrate = Migrate()

from .user import User, Role
from .chapter import Chapter
from .venue import Venue
from .character import Character

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
