import os
from blinker import Namespace
from flask import Flask
from flask_wtf import CsrfProtect
from werkzeug.utils import import_string

willow_signals = Namespace()

def create_app():
    app = Flask(__name__, static_folder='public')
    
    app.environment = os.getenv('WILLOW_ENV', 'Dev')

    if app.environment != 'Test':
        CsrfProtect(app)

    app.config.from_object('willow.settings.{}Config'.format(app.environment))

    from willow.models import db, login_manager
    db.init_app(app)
    login_manager.init_app(app)

    # import plugins

    app.loaded_plugins = {}
    app.admin_user_hooks = []
    app.dashboard_hooks = []
    app.character_hooks = []
    app.navbar = {'admin': [], 'extra': []}

    for plugin in app.config['PLUGINS']:
        imported_plugin = import_string(plugin)()
        imported_plugin.init_app(app)
        app.loaded_plugins[plugin] = imported_plugin

    # import blueprints
    # Note that plugins should do this automatically, 
    # this is for internal blueprints.
    from willow.blueprints import AccountView
    AccountView.register(app)

    return app
