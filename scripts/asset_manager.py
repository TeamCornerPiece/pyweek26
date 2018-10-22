
import os
import random

from gl import *
from scripts import objloader


def hash_filename(filename):
    random.seed(filename)
    return random.randint(1000000, 9999999)


class AssetManager:
    '''
    Handles loading and saving assets used in the game
    '''

    def __init__(self):
        self.meshes = {}
        self.textures = {}

        self.loaded_filenames = []

        quadVertices = np.array([-0.5, -0.5, 0, 0.5, -0.5, 0, -0.5, 0.5, 0, 0.5, 0.5, 0], np.float32)
        quadNormals = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], np.float32)
        quadIndices = np.array([0, 1, 2, 2, 1, 3], np.uint32)

        self.quad_vao = createMesh(quadVertices, quadNormals, quadIndices)
        self.len_quad_indices = len(quadIndices)

    def get_mesh_id(self, fn: str):
        fn = os.path.join(*fn.split('/'))
        mesh_id = hash_filename(fn)
        if mesh_id not in self.meshes:
            self.loaded_filenames.append(fn)
            self.meshes[mesh_id] = []

            obj = objloader.ObjFile(fn)
            for o in obj.objects.values():
                self.meshes[mesh_id].append((createMesh(np.array(o.vertices, np.float32).flatten(),
                                                        np.array(o.normals, np.float32).flatten(),
                                                        np.array(o.indices, np.uint32).flatten()),
                                             len(o.indices)))

        return mesh_id

    def get_mesh_data(self, mesh_id):
        assert mesh_id in self.meshes, 'invalid mesh_id'
        return self.meshes[mesh_id]
