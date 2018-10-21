

class System:
    def __init__(self, engine):
        self.engine = engine
        self.callbacks = {}
        self.settings = {'active': True}
        self.init()

    def init(self):
        pass

    def add_settings(self, **kwargs):
        for key, value in kwargs.items():
            self.settings[key] = value