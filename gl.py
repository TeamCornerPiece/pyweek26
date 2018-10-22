'''
    Written for PyOpenGL 3.X versions
'''

from OpenGL.GL import *
import numpy as np
import glm

def createShader(string: str, type: any):
    shader = glCreateShader(type)
    glShaderSource(shader, string)
    glCompileShader(shader)

    success = glGetShaderiv(shader=shader, pname=GL_COMPILE_STATUS)
    if success == GL_FALSE:
        print(glGetShaderInfoLog(obj=shader).decode('utf-8'))
        glDeleteShader(shader)

    return shader


def createPipeline(shaders: list):
    program = glCreateProgram()
    for shader in shaders:
        glAttachShader(program, shader)

    glLinkProgram(program)
    success = glGetProgramiv(program, GL_LINK_STATUS)
    if success == GL_FALSE:
        print(glGetProgramInfoLog(obj=program).decode('utf-8'))

        for shader in shaders:
            glDetachShader(program, shader)
        glDeleteProgram(program)

    return program


def createTexture(pixels: np.ndarray, width: int, height: int, filter: GLint, wrap: GLint):
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, width, height, 0, GL_RGBA,
                 GL_UNSIGNED_BYTE, pixels)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, wrap)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, wrap)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, filter)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, filter)

    return texture


def createMesh(positions, texCoords, normals, indices):
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbos = glGenBuffers(4)
    glBindBuffer(GL_ARRAY_BUFFER, vbos[0])
    glBufferData(GL_ARRAY_BUFFER, len(positions) * sizeof(ctypes.c_float), positions, GL_STATIC_DRAW)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

    glBindBuffer(GL_ARRAY_BUFFER, vbos[1])
    glBufferData(GL_ARRAY_BUFFER, len(texCoords) * sizeof(ctypes.c_float), texCoords, GL_STATIC_DRAW)
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, None)

    glBindBuffer(GL_ARRAY_BUFFER, vbos[2])
    glBufferData(GL_ARRAY_BUFFER, len(normals) * sizeof(ctypes.c_float), normals, GL_STATIC_DRAW)
    glEnableVertexAttribArray(2)
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, None)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, vbos[3])
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * sizeof(ctypes.c_uint32), indices, GL_STATIC_DRAW)

    glBindVertexArray(0)

    return vao