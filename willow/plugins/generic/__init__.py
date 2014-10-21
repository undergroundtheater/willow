from werkzeug.utils import import_string
from willow.models import db

class GenericPlugin(object):
    has_models = True
    model_names = [
            'willow.plugins.generic.models.TraitType',
            'willow.plugins.generic.models.GenericTrait',
            ]

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

        if not hasattr(app, 'calculate_user_hooks'):
            app.calculate_character_hooks = [self.calculate_character_hook]

        else:
            app.calculate_character_hooks = [self.calculate_character_hook]

    def calculate_character_hook(self, character):
        cost = 0
        if hasattr(character, 'generic_traits'):
            for trait in character.generic_traits:
                cost += trait.calculate_cost()
    
