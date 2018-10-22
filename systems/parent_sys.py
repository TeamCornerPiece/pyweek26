import glm

from scripts import (
    ecs,
)

from systems.base_sys import System
from scripts.callbacks import *
from scripts.components import *


class ParentSys(System):
    def init(self):
        self.callbacks = {CB_UPDATE: self.update}

    def update(self, ecs_data: ecs.ECS, dt: float):
        for ent_id in ecs_data.get_entities(COMP_PARENT, COMP_TRANSFORM):
            parent_data = ecs_data.get_component_data(ent_id, COMP_PARENT)
            if parent_data:
                parent_trans_data = ecs_data.get_component_data(parent_data[PARENT_ENT_ID],
                                                                COMP_TRANSFORM)
                if parent_trans_data:
                    ecs_data.set_component_data(ent_id, COMP_TRANSFORM,
                                                TRANSFORM_X=parent_trans_data[TRANSFORM_X] +
                                                            parent_data[PARENT_OFFSET_X],
                                                TRANSFORM_Y=parent_trans_data[TRANSFORM_Y] +
                                                            parent_data[PARENT_OFFSET_Y],
                                                TRANSFORM_Z=parent_trans_data[TRANSFORM_Z] +
                                                            parent_data[PARENT_OFFSET_Z],
                                                )
