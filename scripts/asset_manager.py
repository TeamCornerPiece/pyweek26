from gl import *


class AssetManager:
    '''
    Handles loading and saving assets used in the game
    '''

    def __init__(self):
        self.meshes = {}
        self.mesh_ids = {}
        self.mesh_count = 0

        self.textures = {}

        quadVertices = np.array([-0.5, -0.5, 0, 0.5, -0.5, 0, -0.5, 0.5, 0, 0.5, 0.5, 0], np.float32)
        quadNormals = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], np.float32)
        quadIndices = np.array([0, 1, 2, 2, 1, 3], np.uint32)

        self.quad_vao = createMesh(quadVertices, quadNormals, quadIndices)
        self.len_quad_indices = len(quadIndices)
