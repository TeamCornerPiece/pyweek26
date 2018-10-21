from gl import *
from scripts import objloader


class AssetManager:
    '''
    Handles loading and saving assets used in the game
    '''

    def __init__(self):
        self.meshes = {}
        self.textures = {}

        quadVertices = np.array([-0.5, -0.5, 0, 0.5, -0.5, 0, -0.5, 0.5, 0, 0.5, 0.5, 0], np.float32)
        quadNormals = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], np.float32)
        quadIndices = np.array([0, 1, 2, 2, 1, 3], np.uint32)

        self.quad_vao = createMesh(quadVertices, quadNormals, quadIndices)
        self.len_quad_indices = len(quadIndices)

    def get_mesh_id(self, filename: str):
        mesh_id = hash(filename)
        if mesh_id not in self.meshes:
            self.meshes[mesh_id] = []

            obj = objloader.ObjFile(filename)
            for o in obj.objects.values():
                self.meshes[mesh_id].append((createMesh(np.array(o.vertices, np.float32).flatten(),
                                                        np.array(o.normals, np.float32).flatten(),
                                                        np.array(o.indices, np.uint32).flatten()),
                                             len(o.indices)))

        return mesh_id

    def get_mesh_data(self, mesh_id):
        assert mesh_id in self.meshes, 'invalid mesh_id'
        return self.meshes[mesh_id]
