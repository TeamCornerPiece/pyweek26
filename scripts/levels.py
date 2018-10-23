import random
import glm

from scripts.components import *
from scripts.callbacks import *


def test_level(engine):
    # PLAYER

    ent_id = engine.ecs_data.add_entity()
    player_ent_id = ent_id

    engine.ecs_data.add_components(ent_id,
                                   COMP_PLAYER,
                                   COMP_TRANSFORM,
                                   COMP_MESH,
                                   COMP_SHAPE,
                                   COMP_INPUT)

    engine.ecs_data.set_component_data(ent_id, COMP_PLAYER,
                                       PLAYER_ACCEL_INPUT=0,
                                       PLAYER_ACCEL_FORCE=400,
                                       PLAYER_REVERSE_INPUT=0,
                                       PLAYER_REVERSE_FORCE=60,
                                       PLAYER_TURN_INPUT=0,
                                       PLAYER_TURN_FORCE=200,
                                       )

    engine.ecs_data.set_component_data(ent_id, COMP_INPUT,
                                       INPUT_ID=1,
                                       INPUT_X=0,
                                       INPUT_Y=0)

    engine.ecs_data.set_component_data(ent_id, COMP_MESH,
                                       MESH_ID=engine.assets.get_mesh_id('models/chaynik/Chaynik.obj'),
                                       MESH_TEX_ID=engine.assets.get_texture_id('textures/teapot.png')
                                       )

    engine.ecs_data.set_component_data(ent_id, COMP_TRANSFORM,
                                       TRANSFORM_X=0,
                                       TRANSFORM_Y=-.5,
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
                                       SHAPE_DX=0,
                                       SHAPE_DY=0,
                                       SHAPE_DA=0,
                                       SHAPE_ELASTICITY=0.2,
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
                                       CAMERA_DELTA_DIST=0,
                                       CAMERA_MIN_PITCH=glm.radians(15),
                                       CAMERA_MAX_PITCH=glm.radians(60),
                                       )

    engine.ecs_data.set_component_data(ent_id, COMP_TRANSFORM,
                                       TRANSFORM_X=0,
                                       TRANSFORM_Y=1 * 5,
                                       TRANSFORM_Z=1 * 5,
                                       TRANSFORM_PITCH=30 / 57.3,
                                       TRANSFORM_YAW=0.0 / 57.3)

    engine.ecs_data.set_component_data(ent_id, COMP_INPUT,
                                       INPUT_ID=1,
                                       INPUT_X=0,
                                       INPUT_Y=0)

    engine.ecs_data.set_component_data(ent_id, COMP_PARENT,
                                       PARENT_ENT_ID=player_ent_id,
                                       PARENT_OFFSET_X=0,
                                       PARENT_OFFSET_Y=1,
                                       PARENT_OFFSET_Z=0,
                                       )


    # WATER

    ent_id = engine.ecs_data.add_entity()
    engine.ecs_data.add_components(ent_id,
                                   COMP_MESH,
                                   COMP_TRANSFORM,
                                   COMP_SHAPE)

    engine.ecs_data.set_component_data(ent_id, COMP_MESH,
                                       MESH_ID=engine.assets.get_mesh_id('models/cube.obj'),
                                       MESH_TEX_ID=engine.assets.get_texture_id('textures/water.png'),
                                       )

    engine.ecs_data.set_component_data(ent_id, COMP_TRANSFORM,
                                       TRANSFORM_X=0,
                                       TRANSFORM_Y=0,
                                       TRANSFORM_Z=0,
                                       TRANSFORM_PITCH=0,
                                       TRANSFORM_YAW=0,
                                       TRANSFORM_SX=30,
                                       TRANSFORM_SY=.1,
                                       TRANSFORM_SZ=185)

    # TEST TREE

    for x in (-1, 1):
        for z in range(-10, 11):
            ent_id = engine.ecs_data.add_entity()
            engine.ecs_data.add_components(ent_id,
                                           COMP_MESH,
                                           COMP_TRANSFORM,
                                           COMP_SHAPE)

            engine.ecs_data.set_component_data(ent_id, COMP_MESH,
                                               MESH_ID=engine.assets.get_mesh_id('models/tree_1.obj'),
                                               MESH_TEX_ID=engine.assets.get_texture_id('textures/rock.png'),
                                               )

            scale = 1 + random.random() * 2

            engine.ecs_data.set_component_data(ent_id, COMP_TRANSFORM,
                                               TRANSFORM_X=(x * 25) + random.random() * 5,
                                               TRANSFORM_Y=0,
                                               TRANSFORM_Z=(z * 5) + random.random() * 3,
                                               TRANSFORM_PITCH=0,
                                               TRANSFORM_YAW=random.random() * 3.14,
                                               TRANSFORM_SX=scale,
                                               TRANSFORM_SY=scale,
                                               TRANSFORM_SZ=scale)


    for x in (-1, 1):
        for y in range(-50, 51):
            ent_id = engine.ecs_data.add_entity()
            engine.ecs_data.add_components(ent_id,
                                           COMP_MESH,
                                           COMP_TRANSFORM,
                                           COMP_SHAPE)

            engine.ecs_data.set_component_data(ent_id, COMP_MESH,
                                               MESH_ID=engine.assets.get_mesh_id('models/rock.obj'),
                                               MESH_TEX_ID=engine.assets.get_texture_id('textures/rock.png'),
                                               )

            scale = 4 + random.random() * 5

            engine.ecs_data.set_component_data(ent_id, COMP_TRANSFORM,
                                               TRANSFORM_X=(x * scale * 2) + random.random() * 5,
                                               TRANSFORM_Y=0,
                                               TRANSFORM_Z=y * 2,
                                               TRANSFORM_PITCH=0,
                                               TRANSFORM_YAW=random.random() * 3.14,
                                               TRANSFORM_SX=scale,
                                               TRANSFORM_SY=scale,
                                               TRANSFORM_SZ=scale)

            engine.ecs_data.set_component_data(ent_id, COMP_SHAPE,
                                               SHAPE_TYPE=0,
                                               SHAPE_MASS=-1.0,
                                               SHAPE_RADIUS=scale * .5,
                                               SHAPE_SIZE_X=1,
                                               SHAPE_SIZE_Y=5,
                                               SHAPE_DX=0,
                                               SHAPE_DY=0,
                                               SHAPE_DA=0,
                                               SHAPE_ELASTICITY=1.0,
                                               SHAPE_FRICTION=1.0,
                                               )

            engine.dispatch(CB_ADD_PHYSICS_ENT, [ent_id])


LEVELS = {
    'test_level': test_level,
}
