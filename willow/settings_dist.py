import datetime
import os

class BaseConfig(object):
    """ File based configuration object."""

    SECRET_KEY = ''

    APP_DIR = os.path.abspath(os.path.dirname(__file__))

    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR,os.pardir))

    DEBUG = os.getenv('DEBUG', True)

    SQLALCHEMY_DATABASE_URI = 'sqlite:///willow_db.sqlite'

    SQLALCHEMY_ECHO = DEBUG

    PLUGINS = []
     
    # Example using provided plugins:
    # PLUGINS = ['willow.plugins.generic.GenericPlugin']

    CHARGEN_MANAGER = 'willow.chargen.ChargenManager'

    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'example'
    MAIL_PASSWORD = 'example'

class DevConfig(BaseConfig):
    SQLALCHEMY_ECHO = False
    DEBUG = True

class TestConfig(BaseConfig):
    SECRET_KEY = 'TEST'
    DEBUG = True
    WTF_CSRF_ENABLED = False
