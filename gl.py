from OpenGL.GL import *


def createShader(string: str, type: any):
    shader = glCreateShader(type)
    glShaderSource(shader, string)
    glCompileShader(shader)

    success = glGetShaderiv(GL_COMPILE_STATUS)
    if success == GL_FALSE:
        print(glGetShaderInfoLog(shader).decode('utf-8'))
        glDeleteShader(shader)

    return shader

def createPipeline(shaders: list):
    program = glCreateProgram()
    for shader in shaders:
        glLinkProgram(program, shader)

