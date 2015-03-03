import datetime
import os

# Copy this file to willow/settings.py to run the application.
# Note that this assumes you've got your python environment
# configured using everything in requirements.txt. See README
# for more information (some day soon).

# DO NOT run in production without reading SECRET_KEY, below.

# The idea is to sub-class BaseConfig and use that as your
# configuration object when initalizing flask in its production
# python container.  See the flask documentation for more
# detailed information.

# Use WILLOW_ENV in your OS environment to determine the class
# imported at run-time.  You should use BaseConfig as a model for
# what you can modify and include.  Take a look at documentation
# for the various flask extensions in requirements.txt for more
# options and help.

class BaseConfig(object):
    """ File based configuration object."""

    # Required - make this a random, unique string in production.
    SECRET_KEY = 'TEST0.2'

    APP_DIR = os.path.abspath(os.path.dirname(__file__))

    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR,os.pardir))

    DEBUG = os.getenv('DEBUG', True)

    SQLALCHEMY_DATABASE_URI = 'sqlite:///willow_db.sqlite'

    SQLALCHEMY_ECHO = DEBUG

    PLUGINS = []

    # Optional.  Required for some plugins.
    PROFILE_MODEL = 'willow.plugins.generic.models.Profile'
     
    # Example using provided plugins:
    # PLUGINS = ['willow.plugins.generic.GenericPlugin']

    CHARGEN_VIEW = 'willow.blueprints.chargen.ChargenView'

    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'example'
    MAIL_PASSWORD = 'example'

    # Flask-Security Necessities
    SECURITY_REGISTERABLE = True
    SECURITY_CHANGEABLE = True

class DevConfig(BaseConfig):
    SQLALCHEMY_ECHO = False
    DEBUG = True

    # Change for production to allow emails to be sent.
    SECURITY_CONFIRMABLE = False

    # Change for production
    SECURITY_PASSWORD_HASH = 'plaintext'

class TestConfig(BaseConfig):
    SECRET_KEY = 'TEST'
    DEBUG = True
    WTF_CSRF_ENABLED = False
