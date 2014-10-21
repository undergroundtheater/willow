class BaseChargenManager(object):

    chargen_hooks = []

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        if not hasattr(self.app, 'chargen_hooks'):
            self.chargen_hooks = []

    def process_chargen(self, **kwargs):
        raise NotImplementedError

class ChargenManager(BaseChargenManager):

    def process_chargen(self, **kwargs):
        for hook in self.app.chargen_hooks:
            kwargs.update(hook(**kwargs))

        return kwargs

