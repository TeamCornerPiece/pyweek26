from scripts import (
    ecs,
)

from systems.base_sys import System
from scripts.callbacks import *
from scripts.levels import *


class LevelSys(System):
    def init(self):
        self.callbacks = {CB_LOAD_LEVEL: self.load_level}

    def load_level(self, ecs_data: ecs.ECS, level_name: str):
        pass

