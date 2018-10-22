from scripts import (
    ecs,
)

from systems.base_sys import System
from scripts.callbacks import *
from scripts.components import *


class CameraMovement(System):
    def init(self):
        self.callbacks = {
            CB_CAMERA_TURN: self.camera_turn,
        }

    def camera_turn(self, ecs_data: ecs.ECS, pitch: float, yaw: float, controller_id: int):
        for ent_id in ecs_data.get_entities(COMP_CAMERA, COMP_INPUT, COMP_TRANSFORM):
            input_data = ecs_data.get_component_data(ent_id, COMP_INPUT)
            if input_data and input_data[INPUT_ID] == controller_id:
                trans_data = ecs_data.get_component_data(ent_id, COMP_TRANSFORM)
                trans_data[TRANSFORM_PITCH] += pitch
                trans_data[TRANSFORM_YAW] += yaw

