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
            app.calculate_character_hooks.append(self.calculate_character_hook)

        if not hasattr(app, 'chargen_hooks'):
            app.chargen_hooks = [self.chargen_hook]
        else:
            app.chargen_hooks.append(self.chargen_hook)

    def calculate_character_hook(self, **kwargs):
        xpspent = 0
        xpgained = 0
#         if hasattr(character, 'generic_traits'):
#             for trait in character.generic_traits:
#                 cost = trait.calculate_cost()
#                 if cost < 0:
#                     xpgained += abs(cost)
#                 else:
#                     xpspent += cost



        return kwargs.update({'xpspent': xpspent, 'xpgained': xpgained})

    def chargen_hook(self, **kwargs):
        # TODO - for 0.2
        return kwargs
    
