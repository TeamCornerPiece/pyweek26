from scripts import (
    ecs,
)

from systems.base_sys import System
from scripts.callbacks import *
from scripts.components import *


class PlayerMovementSys(System):
    """
    updates the pymunk physics space and dispatches physics related callbacks
    """

    def init(self):
        self.callbacks = {
            CB_PLAYER_SET_ACCEL: self.player_accel,
            CB_PLAYER_SET_REVERSE: self.player_reverse,

            CB_UPDATE: self.update,
        }

    def update(self, ecs_data: ecs.ECS, dt: float):
        pass

    def player_accel(self, ecs_data: ecs.ECS, value: float, controller_id: int):
        for ent_id in ecs_data.get_entities(COMP_PLAYER, COMP_INPUT):
            input_data = ecs_data.get_component_data(ent_id, COMP_INPUT)
            if input_data and input_data[INPUT_ID] == controller_id:
                player_data = ecs_data.get_component_data(ent_id, COMP_PLAYER)
                if player_data:
                    player_data[PLAYER_ACCEL_INPUT] = value

    def player_reverse(self, ecs_data: ecs.ECS, value: float, controller_id: int):
        for ent_id in ecs_data.get_entities(COMP_PLAYER, COMP_INPUT):
            input_data = ecs_data.get_component_data(ent_id, COMP_INPUT)
            if input_data and input_data[INPUT_ID] == controller_id:
                player_data = ecs_data.get_component_data(ent_id, COMP_PLAYER)
                if player_data:
                    player_data[PLAYER_REVERSE_INPUT] = value
