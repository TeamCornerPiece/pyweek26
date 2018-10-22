from scripts.components import *
from scripts.callbacks import *
import os

def test_level(engine):
    # PLAYER

    ent_id = engine.ecs_data.add_entity()
    # add components to entity
    engine.ecs_data.add_components(ent_id,
                                   COMP_TRANSFORM,
                                   COMP_MESH,
                                   COMP_SHAPE)
    # get/set mesh component data
    mesh_data = engine.ecs_data.get_component_data(ent_id, COMP_MESH)
    # mesh_data[MESH_ID] = self.engine.assets.get_mesh_id('models\\test_sphere.obj')
    mesh_data[MESH_ID] = engine.assets.get_mesh_id(os.path.join('models', 'chaynik', 'Chaynik.obj'))

    engine.ecs_data.set_component_data(ent_id, COMP_TRANSFORM,
                                       0, 0, 1,
                                       0, 0,
                                       1, 1, 1)

    engine.ecs_data.set_component_data(ent_id, COMP_SHAPE,
                                       SHAPE_TYPE=0,
                                       SHAPE_MASS=1.0,
                                       SHAPE_RADIUS=0.1,
                                       SHAPE_DX=0.5,
                                       SHAPE_DY=0,
                                       SHAPE_DA=0,
                                       SHAPE_ELASTICITY=1.0,
                                       SHAPE_FRICTION=1.0,
                                       )

    engine.dispatch(CB_ADD_PHYSICS_ENT, [ent_id])


    # WALL CUBE

    ent_id = engine.ecs_data.add_entity()
    engine.ecs_data.add_components(ent_id,
                                   COMP_MESH,
                                   COMP_TRANSFORM,
                                   COMP_SHAPE)

    engine.ecs_data.set_component_data(ent_id, COMP_MESH,
                                       MESH_ID=engine.assets.get_mesh_id(os.path.join('models', 'cube.obj')))

    engine.ecs_data.set_component_data(ent_id, COMP_TRANSFORM,
                                       3, 0, 0,
                                       0, -30.0 / 57.3,
                                       1, 2, 5)

    engine.ecs_data.set_component_data(ent_id, COMP_SHAPE,
                                       SHAPE_TYPE=1,
                                       SHAPE_MASS=1.0,
                                       SHAPE_RADIUS=1.0,
                                       SHAPE_SIZE_X=1,
                                       SHAPE_SIZE_Y=5,
                                       SHAPE_DX=0,
                                       SHAPE_DY=0,
                                       SHAPE_DA=0,
                                       SHAPE_ELASTICITY=1.0,
                                       SHAPE_FRICTION=1.0,
                                       )

    engine.dispatch(CB_ADD_PHYSICS_ENT, [ent_id])

    # WALL CUBE 2

    ent_id = engine.ecs_data.add_entity()
    engine.ecs_data.add_components(ent_id,
                                   COMP_MESH,
                                   COMP_TRANSFORM,
                                   COMP_SHAPE)

    engine.ecs_data.set_component_data(ent_id, COMP_MESH,
                                       MESH_ID=engine.assets.get_mesh_id(os.path.join('models', 'cube.obj')))

    engine.ecs_data.set_component_data(ent_id, COMP_TRANSFORM,
                                       -3, 0, 0,
                                       0, 0,
                                       1, 2, 5)

    engine.ecs_data.set_component_data(ent_id, COMP_SHAPE,
                                       SHAPE_TYPE=1,
                                       SHAPE_MASS=1.0,
                                       SHAPE_RADIUS=1.0,
                                       SHAPE_SIZE_X=1,
                                       SHAPE_SIZE_Y=5,
                                       SHAPE_DX=0,
                                       SHAPE_DY=0,
                                       SHAPE_DA=0,
                                       SHAPE_ELASTICITY=1.0,
                                       SHAPE_FRICTION=1.0,
                                       )

    engine.dispatch(CB_ADD_PHYSICS_ENT, [ent_id])



    # CAMERA

    ent_id = engine.ecs_data.add_entity()
    # add components to camera entity
    engine.ecs_data.add_components(ent_id,
                                   COMP_CAMERA,
                                   COMP_TRANSFORM)
    # get/set camera component data
    cam_data = engine.ecs_data.get_component_data(ent_id, COMP_CAMERA)
    cam_data[CAMERA_FOV] = 70.0 / 57.3
    cam_data[CAMERA_NEAR] = 0.01
    cam_data[CAMERA_FAR] = 10.0

    trans_data = engine.ecs_data.get_component_data(ent_id, COMP_TRANSFORM)
    trans_data[TRANSFORM_X] = 0
    trans_data[TRANSFORM_Y] = 2 * 5
    trans_data[TRANSFORM_Z] = 0 * 5
    trans_data[TRANSFORM_PITCH] = 90 / 57.3
    trans_data[TRANSFORM_YAW] = 0.0 / 57.3


LEVELS = {
    'test_level': test_level,
}
