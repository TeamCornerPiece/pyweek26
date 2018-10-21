from scripts.components import *


def test_level(engine):
    # add new entity
    ent_id = engine.ecs_data.add_entity()
    # add components to entity
    engine.ecs_data.add_components(ent_id, COMP_TRANSFORM, COMP_MESH)
    # get/set mesh component data
    mesh_data = engine.ecs_data.get_component_data(ent_id, COMP_MESH)
    # mesh_data[MESH_ID] = self.engine.assets.get_mesh_id('models\\test_sphere.obj')
    mesh_data[MESH_ID] = engine.assets.get_mesh_id('models\\chaynik\\Chaynik.obj')

    # add entity for camera
    ent_id = engine.ecs_data.add_entity()
    # add components to camera entity
    engine.ecs_data.add_components(ent_id,
                                   COMP_CAMERA,
                                   COMP_TRANSFORM)
    # get/set camera component data
    cam_data = engine.ecs_data.get_component_data(ent_id, COMP_CAMERA)
    cam_data[CAMERA_FOV] = 45.0 / 57.3
    cam_data[CAMERA_NEAR] = 0.1
    cam_data[CAMERA_FAR] = 1000.0

    trans_data = engine.ecs_data.get_component_data(ent_id, COMP_TRANSFORM)
    trans_data[TRANSFORM_X] = 0
    trans_data[TRANSFORM_Y] = 0
    trans_data[TRANSFORM_Z] = 1
    trans_data[TRANSFORM_PITCH] = 0
    trans_data[TRANSFORM_YAW] = 180.0 / 57.3


LEVELS = {
    'test_level': test_level,
}
