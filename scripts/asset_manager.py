import os
import random

from PIL import Image

from gl import *
from scripts import objloader

import hashlib


def hash_filename(filename):
    return hashlib.sha1(filename.encode()).hexdigest()


class AssetManager:
    '''
    Handles loading and saving assets used in the game
    '''

    def __init__(self):
        self.meshes = []
        self.textures = []

        self.mesh_ids = {}
        self.tex_ids = {}

        self.mesh_count = 0
        self.texture_count = 0

        quadVertices = np.array([-0.5, -0.5, 0, 0.5, -0.5, 0, -0.5, 0.5, 0, 0.5, 0.5, 0], np.float32)
        quadNormals = np.array([0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1], np.float32)
        quadTexCoords = np.array([0, 0, 1, 0, 0, 1, 1, 1], np.float32)
        quadIndices = np.array([0, 1, 2, 2, 1, 3], np.uint32)

        self.quad_vao = createMesh(quadVertices, quadTexCoords, quadNormals, quadIndices)
        self.len_quad_indices = len(quadIndices)

    def get_mesh_id(self, fn: str):
        fn = os.path.join(*fn.split('/'))
        mesh_id = self.mesh_ids.get(fn, -1)
        if mesh_id == -1:
            mesh_id = self.mesh_count
            self.mesh_ids[fn] = self.mesh_count
            self.mesh_count += 1

            self.meshes.append([])

            obj = objloader.ObjFile(fn)
            for o in obj.objects.values():
                self.meshes[-1].append((createMesh(np.array(o.vertices, np.float32).flatten(),
                                               np.array(o.texcoords, np.float32).flatten(),
                                               np.array(o.normals, np.float32).flatten(),
                                               np.array(o.indices, np.uint32).flatten()),
                                    len(o.indices)))

        return mesh_id

    def get_texture_id(self, file_name: str):
        file_name = os.path.join(*file_name.split('/'))
        texture_id = self.tex_ids.get(file_name, -1)
        if texture_id == -1:
            texture_id = self.texture_count
            self.tex_ids[file_name] = self.texture_count
            self.texture_count += 1

            image = Image.open(file_name)
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
            image = image.convert("RGBA")

            pixels = np.array(list(image.getdata()), np.uint8)
            self.textures.append(createTexture(pixels,
                                               image.width,
                                               image.height,
                                               GL_LINEAR,
                                               GL_CLAMP_TO_EDGE))
        return texture_id

    def get_texture_data(self, tex_id):
        assert 0 <= tex_id < len(self.textures), 'invalid texture_id'
        return self.textures[tex_id]

    def get_mesh_data(self, mesh_id):
        assert 0 <= mesh_id < len(self.meshes), 'invalid mesh_id'
        return self.meshes[mesh_id]
