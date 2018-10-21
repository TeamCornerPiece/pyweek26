from scripts import (
    ecs,
)

from systems.base_sys import System
from scripts.callbacks import *
from scripts.components import *


class LevelSys(System):
    def init(self):
        self.callbacks = {CB_LOAD_LEVEL: self.load_level}

    def load_level(self, ecs_data: ecs.ECS, level_name: str):
        ent_id = ecs_data.add_entity()
        ecs_data.add_components(ent_id, COMP_TRANSFORM)

        ent_id = ecs_data.add_entity()
        ecs_data.add_components(ent_id,
                                COMP_CAMERA,
                                COMP_TRANSFORM)
        cam_data = ecs_data.get_component_data(ent_id, COMP_CAMERA)
        cam_data[CAMERA_FOV] = 90 / 57.3
