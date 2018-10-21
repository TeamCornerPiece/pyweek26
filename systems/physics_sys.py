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

        self.bodies = {}
        self.body_index = 0

        self.callbacks = {
            CB_UPDATE: self.update,
            CB_ADD_PHYSICS_ENT: self.add_physics_ent,
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
                rbody_id = shape_data[SHAPE_BODY_ID]
                mass = shape_data[SHAPE_MASS]
                if rbody_id >= 0 and mass > 0:
                    body = self.bodies.get(rbody_id)
                    if body:
                        trans_data = ecs_data.get_component_data(ent_id,
                                                                 COMP_TRANSFORM)
                        if trans_data:
                            trans_data[TRANSFORM_X] = body.position.x
                            trans_data[TRANSFORM_Z] = body.position.y
                            trans_data[TRANSFORM_YAW] = -body.angle

    def add_physics_ent(self, ecs_data: ecs.ECS, ent_id: int):
        shape_data = ecs_data.get_component_data(ent_id, COMP_SHAPE)

        if shape_data:
            pos = (0, 0)

            trans_data = ecs_data.get_component_data(ent_id, COMP_TRANSFORM)
            if trans_data:
                pos = trans_data[TRANSFORM_X], trans_data[TRANSFORM_Z]

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
                else:
                    shape = pymunk.Poly.create_box(body, (size_x, size_y))
                    shape.mass = mass

            if mass >= 0:
                self.space.add(body)
                body.position = pos
                body.velocity = shape_data[SHAPE_DX:SHAPE_DY + 1]
                print(shape_data[SHAPE_DX:SHAPE_DY + 1])

                self.bodies[self.body_index] = body
                shape_data[SHAPE_BODY_ID] = self.body_index
                self.body_index += 1

            elasticity = shape_data[SHAPE_ELASTICITY]
            if elasticity < 0:
                elasticity = 1.0

            friction = shape_data[SHAPE_FRICTION]
            if friction < 0:
                friction = 1.0

            shape.elasticity = elasticity
            shape.friction = friction
            self.space.add(shape)

            print('ent_id: {}'.format(ent_id))
            print('shape: {}'.format(shape_data))
