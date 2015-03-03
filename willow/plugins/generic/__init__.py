from werkzeug.utils import import_string
from willow.models import db
from willow.models.user import Role, User
from .views import generic_blueprint

class GenericPlugin(object):
    has_models = True
    model_names = [
            'willow.plugins.generic.models.Profile',
            'willow.plugins.generic.models.TraitType',
            'willow.plugins.generic.models.GenericTrait',
            ]

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

        app.register_blueprint(generic_blueprint, url_prefix='/gen')
        app.navbar['admin'].insert(0,
                (
                    '',
                    'Users',
                    'generic.AdminUserListView:index',))

        if getattr(app, 'calculate_user_hooks', False):
            app.calculate_character_hooks.append(self.calculate_character_hook)
        else:
            app.calculate_character_hooks = [self.calculate_character_hook]

        if getattr(app, 'chargen_hooks', False):
            app.chargen_hooks.append(self.chargen_hook)
        else:
            app.chargen_hooks = [self.chargen_hook]

        if getattr(app, 'init_db_hooks', False):
            app.init_db_hooks.append(self.__class__.init_db)
        else:
            app.init_db_hooks = [self.__class__.init_db]

    def calculate_character_hook(self, **kwargs):
        xpspent = 0
        xpgained = 0
        if hasattr(character, 'generic_traits'):
            for trait in character.generic_traits:
                cost = trait.calculate_cost()
                if cost < 0:
                    xpgained += abs(cost)
                else:
                    xpspent += cost

        return kwargs.update({'xpspent': xpspent, 'xpgained': xpgained})

    def chargen_hook(self, **kwargs):
        # TODO - for 0.2
        return kwargs

    @staticmethod
    def init_db(app, db):
        try:
            role = Role(name='Admin', description='Administrator')
            db.session.add(role)
            db.session.commit()
        except:
            db.session.rollback()
            role = Role.query.filter_by(name='Admin')

        user = User.query.get(1)
        user.roles.append(role)
        db.session.add(user)
        db.session.commit()
