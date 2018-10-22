import os
import random

from PIL import Image

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

        self.loaded_textures = []
        self.loaded_filenames = []

        quadVertices = np.array([-0.5, -0.5, 0, 0.5, -0.5, 0, -0.5, 0.5, 0, 0.5, 0.5, 0], np.float32)
        quadNormals = np.array([0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1], np.float32)
        quadTexCoords = np.array([0, 0, 1, 0, 0, 1, 1, 1], np.float32)
        quadIndices = np.array([0, 1, 2, 2, 1, 3], np.uint32)

        self.quad_vao = createMesh(quadVertices, quadTexCoords, quadNormals, quadIndices)
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
                                                        np.array(o.texcoords, np.float32).flatten(),
                                                        np.array(o.normals, np.float32).flatten(),
                                                        np.array(o.indices, np.uint32).flatten()),
                                            len(o.indices)))
        return mesh_id


    def get_texture_id(self, file_name: str):
        file_name = os.path.join(*file_name.split('/'))
        texture_id = hash_filename(file_name)
        if texture_id not in self.textures:
            self.textures[texture_id] = []
            self.loaded_textures.append(file_name)

            image = Image.open(file_name)
            image = image.transpose(Image.FLIP_TOP_BOTTOM)

            pixels = np.array(list(image.getdata()), np.uint8)
            self.textures[texture_id] = createTexture(pixels, image.width, image.height, GL_LINEAR, GL_CLAMP_TO_EDGE)

        return texture_id


    def get_texture_data(self, tex_id):
        print(self.textures)
        assert tex_id in self.textures, 'invalid texture_id'
        return self.textures[tex_id]

    def get_mesh_data(self, mesh_id):
        assert mesh_id in self.meshes, 'invalid mesh_id'
        return self.meshes[mesh_id]
