import os
from blinker import Namespace
from flask import Flask, redirect, url_for, session, request, flash, render_template
from flask_wtf import CsrfProtect
from flask_mail import Mail
from werkzeug.utils import import_string

from flask_security.utils import url_for_security

willow_signals = Namespace()

mail = Mail()

def create_app():
    app = Flask(__name__, static_folder='public')
    
    app.environment = os.getenv('WILLOW_ENV', 'Dev')

    if app.environment != 'Test':
        CsrfProtect(app)

    app.config.from_object('willow.settings.{}Config'.format(app.environment))

    from willow.models import db, user_datastore, security
    db.init_app(app)
    security.init_app(app, user_datastore)
    mail.init_app(app)

    chargen = import_string(app.config.get('CHARGEN_MANAGER'))()

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
        if imported_plugin.has_models:
            with app.app_context():
                for model in imported_plugin.model_names:
                    impmodel = import_string(model)
                    if not impmodel.__table__.exists(db.engine):
                        impmodel.__table__.create(db.engine)

    # import blueprints
    # Note that plugins should do this automatically, 
    # this is for internal blueprints.
    # from willow.blueprints import AccountView
    # AccountView.register(app)

    @app.route('/')
    def home():
        return render_template('willow/home.html')

    @app.context_processor
    def inject_globals():
        return {
                'hooks': {
                    'admin_user_hooks': app.admin_user_hooks,
                    'dashboard_hooks': app.dashboard_hooks
                    },
                'navbar': app.navbar
                }

    @app.before_request
    def check_session():
        if session.get('ip') != request.remote_addr:
            session.clear()
            session['ip'] = request.remote_addr
            flash('Session expired, please login.')
            return redirect(url_for_security('login'))

    return app
