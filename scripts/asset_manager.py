import os
import glm

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
        self.meshes = {}
        self.textures = {}

        self.loaded_meshes = []
        self.loaded_textures = []

        quadVertices = np.array([-0.5, -0.5, 0, 0.5, -0.5, 0, -0.5, 0.5, 0, 0.5, 0.5, 0], np.float32)
        quadNormals = np.array([0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1], np.float32)
        quadTexCoords = np.array([0, 0, 1, 0, 0, 1, 1, 1], np.float32)
        quadIndices = np.array([0, 1, 2, 2, 1, 3], np.uint32)

        self.quad_vao = createMesh(quadVertices, quadTexCoords, quadNormals, quadIndices)
        self.len_quad_indices = len(quadIndices)

        self.river_faces = []
        self.segments = []

    def load_river(self, file_name: str):
        file_name = os.path.join(*file_name.split('/'))

        vertices = []
        faces = []

        with open(file_name, 'r') as f:
            for line in f.readlines():
                args = line.split(' ')
                command = args[0]
                data = args[1:]
                if command == 'v':
                    vertices.append(glm.vec3([float(i) for i in data]))
                elif command == 'f':
                    assert len(data) == 3, 'ALL FACES MUST BE TRIANGULATED'
                    face = []
                    for point in data:
                        index = int(point.split('/')[0]) - 1
                        face.append(index)
                    faces.append(face)

        segments = []
        for f, face in enumerate(faces):
            for i, index in enumerate(face):
                end_index = face[i - 1]
                for o, other_face in enumerate(faces):
                    if o != f:
                        if index in other_face and end_index in other_face:
                            break
                else:
                    segments.append((vertices[end_index].xz,
                                     vertices[index].xz))

        self.river_faces = [[vertices[i] for i in f] for f in faces]
        self.segments = segments

    def get_mesh_id(self, file_name: str):
        file_name = os.path.join(*file_name.split('/'))
        mesh_id = hash_filename(file_name)
        if mesh_id not in self.meshes:
            self.meshes[mesh_id] = []

            obj = objloader.ObjFile(file_name)
            for o in obj.objects.values():
                self.meshes[mesh_id].append((createMesh(np.array(o.vertices, np.float32).flatten(),
                                                        np.array(o.texcoords, np.float32).flatten(),
                                                        np.array(o.normals, np.float32).flatten(),
                                                        np.array(o.indices, np.uint32).flatten()),
                                             len(o.indices)))
        return mesh_id

    def get_texture_id(self, file_name: str):
        file_name = os.path.join(*file_name.split('/'))
        tex_id = hash_filename(file_name)
        if tex_id not in self.textures:
            image = Image.open(file_name)
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
            image = image.convert("RGBA")

            pixels = np.array(list(image.getdata()), np.uint8)
            self.textures[tex_id] = createTexture(pixels,
                                                  image.width,
                                                  image.height,
                                                  GL_LINEAR,
                                                  GL_CLAMP_TO_EDGE)
        return tex_id

    def get_texture_data(self, tex_id):
        assert tex_id in self.textures, 'invalid texture_id'
        return self.textures[tex_id]

    def get_mesh_data(self, mesh_id):
        assert mesh_id in self.meshes, 'invalid mesh_id'
        return self.meshes[mesh_id]
