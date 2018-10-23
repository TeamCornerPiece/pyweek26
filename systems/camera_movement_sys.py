import glm

from scripts import (
    ecs,
)

from systems.base_sys import System
from scripts.callbacks import *
from scripts.components import *


class CameraMovementSys(System):
    def init(self):
        self.callbacks = {
            CB_UPDATE: self.update,
            CB_CAMERA_TURN: self.camera_turn,
            CB_CAMERA_ZOOM: self.camera_zoom,
        }

    def update(self, ecs_data: ecs.ECS, dt: float):
        for ent_id in ecs_data.get_entities(COMP_CAMERA, COMP_TRANSFORM, COMP_INPUT):
            trans_data = ecs_data.get_component_data(ent_id, COMP_TRANSFORM)
            input_data = ecs_data.get_component_data(ent_id, COMP_INPUT)

            if input_data and trans_data:
                min_pitch = -1.57
                max_pitch = 1.57

                cam_data = ecs_data.get_component_data(ent_id, COMP_CAMERA)
                if cam_data:
                    min_pitch = cam_data[CAMERA_MIN_PITCH]
                    max_pitch = cam_data[CAMERA_MAX_PITCH]

                trans_data[TRANSFORM_YAW] += input_data[INPUT_X] * dt * glm.radians(360.0)
                trans_data[TRANSFORM_PITCH] = glm.clamp(trans_data[TRANSFORM_PITCH] +
                                                        input_data[INPUT_Y] * dt * glm.radians(360.0),
                                                        min_pitch, max_pitch)
                if input_data[INPUT_ID] == 0:
                    input_data[INPUT_X] = 0
                    input_data[INPUT_Y] = 0

            cam_data = ecs_data.get_component_data(ent_id, COMP_CAMERA)
            if cam_data:
                cam_data[CAMERA_DIST] = glm.clamp(cam_data[CAMERA_DIST] +
                                                  cam_data[CAMERA_DELTA_DIST] * dt,
                                                  1, 20)


    def camera_turn(self, ecs_data: ecs.ECS, pitch: float, yaw: float, controller_id: int):
        for ent_id in ecs_data.get_entities(COMP_CAMERA, COMP_INPUT, COMP_TRANSFORM):
            input_data = ecs_data.get_component_data(ent_id, COMP_INPUT)
            if input_data and input_data[INPUT_ID] == controller_id:
                trans_data = ecs_data.get_component_data(ent_id, COMP_TRANSFORM)

                input_data[INPUT_X] = yaw
                input_data[INPUT_Y] = pitch

    def camera_zoom(self, ecs_data: ecs.ECS, value: float, controller_id: int):
        for ent_id in ecs_data.get_entities(COMP_CAMERA, COMP_INPUT):
            input_data = ecs_data.get_component_data(ent_id, COMP_INPUT)
            if input_data and input_data[INPUT_ID] == controller_id:
                cam_data = ecs_data.get_component_data(ent_id, COMP_CAMERA)
                cam_data[CAMERA_DELTA_DIST] = value
