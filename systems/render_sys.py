from systems.base_sys import System
from scripts.callbacks import *


class RenderSys(System):
    def init(self):
        self.callbacks = {
            CB_UPDATE: self.update,
        }

    def update(self, ecs_data, dt):
        pass