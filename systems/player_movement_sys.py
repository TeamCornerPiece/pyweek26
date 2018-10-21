from scripts import (
    ecs,
)

from systems.base_sys import System
from scripts.callbacks import *
from scripts.components import *


class PlayerMovement(System):
    """
    updates the pymunk physics space and dispatches physics related callbacks
    """

    def init(self):
        self.callbacks = {
            CB_PLAYER_SET_ACCEL: self.player_accel,
            CB_UPDATE: self.update,
        }

    def update(self, ecs_data: ecs.ECS, dt: float):
        for ent_id in ecs_data.get_entities(COMP_PLAYER, COMP_SHAPE):
            player_data = ecs_data.get_component_data(ent_id, COMP_PLAYER)
            if player_data:
                force = player_data[PLAYER_ACCEL_INPUT] * player_data[PLAYER_ACCEL_FORCE]

    def player_accel(self, ecs_data: ecs.ECS, value: float, controller_id: int):
        for ent_id in ecs_data.get_entities(COMP_PLAYER, COMP_INPUT):
            input_data = ecs_data.get_component_data(ent_id, COMP_INPUT)
            if input_data and input_data[INPUT_ID] == controller_id:
                player_data = ecs_data.get_component_data(ent_id, COMP_PLAYER)
                if player_data:
                    player_data[PLAYER_ACCEL_INPUT] = value
