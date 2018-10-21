from systems.base_sys import System
from scripts.callbacks import *


class RenderSys(System):
    def __init__(self, engine):
        System.__init__(self, engine)
        self.callbacks = {CB_UPDATE: self.update}



    def update(self, ecs_data, dt):
        print(dt)
