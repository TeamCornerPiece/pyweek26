from OpenGL.GL import *
import glm

import numpy as np


def createShader(string, shaderType):
    shader = glCreateShader(shaderType)
    glShaderSource(shader, string)
    glCompileShader(shader)

    if glGetShaderiv(shader, GL_COMPILE_STATUS) == GL_FALSE:
        print("Shader: shader message: %s" % glGetShaderInfoLog(shader).decode("utf-8"))

    return shader


class Shader:
    def __init__(self, fileName):
        self.shaders = []
        self.program = glCreateProgram()

        with open(fileName + ".vert") as content_vert, open(fileName + ".frag") as content_frag:
            self.shaders.append(createShader(content_vert.read(), GL_VERTEX_SHADER))
            self.shaders.append(createShader(content_frag.read(), GL_FRAGMENT_SHADER))
            glAttachShader(self.program, self.shaders[0])
            glAttachShader(self.program, self.shaders[1])

        glLinkProgram(self.program)
        glValidateProgram(self.program)
        if glGetProgramiv(self.program, GL_LINK_STATUS | GL_VALIDATE_STATUS) == GL_FALSE:
            print("Shader: program message: %s" % glGetProgramInfoLog(self.program))

        glDetachShader(self.program, self.shaders[1])
        glDetachShader(self.program, self.shaders[0])

    def __del__(self):
        if glDeleteShader:
            glDeleteShader(self.shaders[1])
            glDeleteShader(self.shaders[0])
        if glDeleteProgram:
            glDeleteProgram(self.program)

    def bind(self):
        glUseProgram(self.program)

    def get_uniform(self, name):
        return glGetUniformLocation(self.program, name)

    def set_mat4(self, name, m):
        glUniformMatrix4fv(glGetUniformLocation(self.program, name),
                           1, False, glm.value_ptr(m))

    def set_mat4_array(self, name, l):
        array = np.empty((len(l), 4, 4), np.float32)

        for i, m in enumerate(l):
            array[i][0] = tuple(m.x)
            array[i][1] = tuple(m.y)
            array[i][2] = tuple(m.z)
            array[i][3] = tuple(m.w)

        glUniformMatrix4fv(glGetUniformLocation(self.program, name),
                           len(l), False, array.flatten())

    def set_int(self, name, i):
        glUniform1i(self.get_uniform(name), i)

    def set_float(self, name, i):
        glUniform1f(self.get_uniform(name), i)

    def set_vec3(self, name, *values):
        glUniform3f(self.get_uniform(name), *values)

    def set_vec3_array(self, name, values):
        glUniform3fv(self.get_uniform(name), len(values) / 3, values)

    def set_vec4(self, name, *values):
        glUniform4f(self.get_uniform(name), *values)


