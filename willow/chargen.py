from willow.models import db, Character

class ChargenManager(object):

    chargen_hooks = []

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        if hasattr(self.app, 'chargen_hooks'):
            self.chargen_hooks = self.app.chargen_hooks
        else:
            self.chargen_hooks = []

    def process_chargen(self, **kwargs):
        for hook in self.chargen_hooks:
            kwargs.update(hook(**kwargs))

        return kwargs
