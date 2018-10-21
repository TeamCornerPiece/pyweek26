
import pymunk

from scripts import (
    ecs,
)

from systems.base_sys import System
from scripts.callbacks import *
from scripts.components import *


class PhysicsSys(System):
    """
    updates the pymunk physics space and dispatches physics related callbacks
    """

    def init(self):
        self.space = pymunk.Space()
        self.space.gravity = 0, -10

        self.callbacks = {CB_UPDATE: self.update}

    def update(self, ecs_data: ecs.ECS, dt: float):
        self.space.step(dt)