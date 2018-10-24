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
        self.space.damping = .5
        self.space.gravity = 0, -2 * 0

        self.shapes = {}
        self.shape_index = 0

        self.callbacks = {
            CB_UPDATE: self.update,
            CB_ADD_PHYSICS_ENT: self.add_physics_ent,
            CB_REMOVE_PHYSICS_ENT: self.remove_shape,
            CB_LOAD_LEVEL: self.load_level,
            CB_SAVE_LEVEL: self.save_level,
        }

        self.box_verts = ((-.5, -.5),
                          (.5, -.5),
                          (-.5, .5),
                          (.5, .5))

    def update(self, ecs_data: ecs.ECS, dt: float):
        self.space.step(dt)

        for ent_id in ecs_data.get_entities(COMP_SHAPE, COMP_TRANSFORM):
            shape_data = ecs_data.get_component_data(ent_id, COMP_SHAPE)
            if shape_data:
                shape_id = shape_data[SHAPE_ID]
                mass = shape_data[SHAPE_MASS]
                if shape_id >= 0 and mass > 0:
                    shape = self.shapes.get(shape_id)
                    if shape and shape.body is not self.space.static_body:
                        trans_data = ecs_data.get_component_data(ent_id,
                                                                 COMP_TRANSFORM)
                        if trans_data:
                            trans_data[TRANSFORM_X] = shape.body.position.x
                            trans_data[TRANSFORM_Z] = shape.body.position.y
                            trans_data[TRANSFORM_YAW] = -shape.body.angle

        for ent_id in ecs_data.get_entities(COMP_PLAYER, COMP_SHAPE):
            player_data = ecs_data.get_component_data(ent_id, COMP_PLAYER)
            if player_data:
                force = player_data[PLAYER_ACCEL_INPUT] * player_data[PLAYER_ACCEL_FORCE] * dt
                force -= player_data[PLAYER_REVERSE_INPUT] * player_data[PLAYER_REVERSE_FORCE] * dt
                turn_force = player_data[PLAYER_TURN_INPUT] * player_data[PLAYER_TURN_FORCE] * dt
                shape_data = ecs_data.get_component_data(ent_id, COMP_SHAPE)
                if shape_data:
                    shape = self.shapes.get(shape_data[SHAPE_ID])
                    if shape and shape.body is not self.space.static_body:
                        shape.body.apply_impulse_at_local_point((0, force))
                        shape.body.angular_velocity += turn_force * dt
                        shape.body.angular_velocity *= 1 - (.9 * dt)


    def add_physics_ent(self, ecs_data: ecs.ECS, ent_id: int):
        shape_data = ecs_data.get_component_data(ent_id, COMP_SHAPE)

        if shape_data:
            pos = (0, 0)
            angle = 0

            trans_data = ecs_data.get_component_data(ent_id, COMP_TRANSFORM)
            if trans_data:
                pos = trans_data[TRANSFORM_X], trans_data[TRANSFORM_Z]
                angle = trans_data[TRANSFORM_YAW]

            mass = shape_data[SHAPE_MASS]
            if mass < 0:
                body = self.space.static_body
            elif mass == 0:
                body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
            else:
                body = pymunk.Body()

            shape_type = shape_data[SHAPE_TYPE]
            assert 0 <= shape_type < 2, 'invalid shape type: {}'.format(shape_type)

            if shape_type == 0:
                radius = shape_data[SHAPE_RADIUS]
                if radius <= 0:
                    radius = 1

                if mass < 0:
                    shape = pymunk.Circle(body, radius, pos)
                else:
                    shape = pymunk.Circle(body, radius)
                    shape.mass = mass

            elif shape_type == 1:
                size_x = shape_data[SHAPE_SIZE_X]
                size_y = shape_data[SHAPE_SIZE_Y]

                if size_x <= 0:
                    size_x = 1
                if size_y <= 0:
                    size_y = 1

                if mass < 0:
                    shape = pymunk.Poly(body, self.box_verts,
                                        pymunk.Transform(a=size_x,
                                                         d=size_y,
                                                         tx=pos[0],
                                                         ty=pos[1])
                                        )
                    # todo: rotate transform to angle ^^^
                else:
                    shape = pymunk.Poly.create_box(body, (size_x, size_y))
                    shape.mass = mass

            if mass >= 0:
                self.space.add(body)
                body.position = pos
                body.angle = -angle
                body.velocity = shape_data[SHAPE_DX:SHAPE_DY + 1]
                body.angular_velocity = shape_data[SHAPE_DA]

            self.shapes[self.shape_index] = shape
            shape_data[SHAPE_ID] = self.shape_index
            self.shape_index += 1

            elasticity = shape_data[SHAPE_ELASTICITY]
            if elasticity < 0:
                elasticity = 1.0

            friction = shape_data[SHAPE_FRICTION]
            if friction < 0:
                friction = 1.0

            shape.elasticity = elasticity
            shape.friction = friction
            self.space.add(shape)

    def remove_shape(self, ecs_data: ecs.ECS, ent_id: int):
        shape_data = ecs_data.get_component_data(ent_id, COMP_SHAPE)
        print(shape_data)
        if shape_data:
            shape_id = shape_data[SHAPE_ID]
            shape = self.shapes.get(shape_id)
            print(shape)
            if shape:
                if shape.body is not self.space.static_body:
                    self.space.remove(shape.body)
                self.space.remove(shape)
                del self.shapes[shape_id]

    def load_level(self, ecs_data: ecs.ECS, filename: str):
        self.space.remove(self.space.bodies,
                          self.space.shapes,
                          self.space.constraints)
        self.shapes = {}
        self.shape_index = 0

        for ent_id in ecs_data.get_entities(COMP_SHAPE):
            shape_data = ecs_data.get_component_data(ent_id, COMP_SHAPE)
            if shape_data:
                self.add_physics_ent(ecs_data, ent_id)



    def save_level(self, ecs_data: ecs.ECS, filename: str):
        for ent_id in ecs_data.get_entities(COMP_SHAPE):
            shape_data = ecs_data.get_component_data(ent_id, COMP_SHAPE)
            if shape_data:
                shape = self.shapes.get(shape_data[SHAPE_ID])
                if shape:
                    shape_data[SHAPE_DX] = shape.body.velocity.x
                    shape_data[SHAPE_DY] = shape.body.velocity.y
                    shape_data[SHAPE_DA] = shape.body.angular_velocity

