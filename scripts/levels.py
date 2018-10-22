from scripts.components import *
from scripts.callbacks import *


def test_level(engine):
    # PLAYER

    ent_id = engine.ecs_data.add_entity()
    # add components to entity
    engine.ecs_data.add_components(ent_id,
                                   COMP_TRANSFORM,
                                   COMP_MESH,
                                   COMP_SHAPE)
    # get/set mesh component data
    engine.ecs_data.set_component_data(ent_id, COMP_MESH,
                                       MESH_ID=engine.assets.get_mesh_id('models/chaynik/Chaynik.obj')
                                       )

    engine.ecs_data.set_component_data(ent_id, COMP_TRANSFORM,
                                       TRANSFORM_X=0,
                                       TRANSFORM_Y=0,
                                       TRANSFORM_Z=1,
                                       TRANSFORM_PITCH=0,
                                       TRANSFORM_YAW=0,
                                       TRANSFORM_SX=1,
                                       TRANSFORM_SY=1,
                                       TRANSFORM_SZ=1)

    engine.ecs_data.set_component_data(ent_id, COMP_SHAPE,
                                       SHAPE_TYPE=0,
                                       SHAPE_MASS=1.0,
                                       SHAPE_RADIUS=1.0,
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
                                       MESH_ID=engine.assets.get_mesh_id('models/cube.obj'),
                                       MESH_SPEC_R=1.0,
                                       MESH_SPEC_G=0.0,
                                       MESH_SPEC_B=0.5,
                                       )

    engine.ecs_data.set_component_data(ent_id, COMP_TRANSFORM,
                                       TRANSFORM_X=3,
                                       TRANSFORM_Y=0,
                                       TRANSFORM_Z=0,
                                       TRANSFORM_PITCH=0,
                                       TRANSFORM_YAW=0,
                                       TRANSFORM_SX=1,
                                       TRANSFORM_SY=2,
                                       TRANSFORM_SZ=5)

    engine.ecs_data.set_component_data(ent_id, COMP_SHAPE,
                                       SHAPE_TYPE=1,
                                       SHAPE_MASS=-1.0,
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
                                       MESH_ID=engine.assets.get_mesh_id('models/cube.obj'))

    engine.ecs_data.set_component_data(ent_id, COMP_TRANSFORM,
                                       TRANSFORM_X=-3,
                                       TRANSFORM_Y=0,
                                       TRANSFORM_Z=0,
                                       TRANSFORM_PITCH=0,
                                       TRANSFORM_YAW=0,
                                       TRANSFORM_SX=1,
                                       TRANSFORM_SY=2,
                                       TRANSFORM_SZ=5)

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
                                   COMP_TRANSFORM,
                                   COMP_INPUT,
                                   COMP_PARENT)

    # get/set camera component data
    engine.ecs_data.set_component_data(ent_id, COMP_CAMERA,
                                       CAMERA_FOV=70.0 / 57.3,
                                       CAMERA_NEAR=0.1,
                                       CAMERA_FAR=1000.0,
                                       CAMERA_DIST=10,
                                       CAMERA_DELTA_DIST=0)

    engine.ecs_data.set_component_data(ent_id, COMP_TRANSFORM,
                                       TRANSFORM_X=0,
                                       TRANSFORM_Y=1 * 5,
                                       TRANSFORM_Z=1 * 5,
                                       TRANSFORM_PITCH=30 / 57.3,
                                       TRANSFORM_YAW=0.0 / 57.3)

    engine.ecs_data.set_component_data(ent_id, COMP_INPUT,
                                       INPUT_ID=0,
                                       INPUT_X=0,
                                       INPUT_Y=0)

    engine.ecs_data.set_component_data(ent_id, COMP_PARENT,
                                       PARENT_ENT_ID=0,
                                       PARENT_OFFSET_X=0,
                                       PARENT_OFFSET_Y=1,
                                       PARENT_OFFSET_Z=0,
                                       )



LEVELS = {
    'test_level': test_level,
}
