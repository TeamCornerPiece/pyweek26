from OpenGL.GL import *


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
    success = glGetProgramiv(program=program, pname=GL_LINK_STATUS)
    if success == GL_FALSE:
        print(glGetProgramInfoLog(obj=program).decode('utf-8'))

        for shader in shaders: glDetachShader(program, shader)
        glDeleteProgram(program)

    return program