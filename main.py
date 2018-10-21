from pyglfw.libapi import *
import math
from gl import *
import glm

quadVertices = np.array([-0.5, -0.5, 0, 0.5, -0.5, 0, -0.5,  0.5, 0, 0.5,  0.5, 0], np.float32)
quadNormals = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], np.float32)
quadIndices = np.array([0, 1, 2, 2, 1, 3], np.uint32)


def euclidean(theta: float, phi: float):
    cosT = math.cos(theta)
    sinT = math.sin(theta)
    cosP = math.cos(phi)
    sinP = math.sin(phi)
    return glm.vec3(cosT * sinT, sinP, cosT * cosP)


if __name__ == '__main__':
    glfwInit()

    major, mintor, rev = glfwGetVersion()

    width = 1280
    height = 720
    aspect = float(width)/height

    window = glfwCreateWindow(width, height, b'Hello World!', None, None)
    glfwMakeContextCurrent(window)

    vertexShader = createShader(open('shaders/default.vert', 'r').read(), GL_VERTEX_SHADER)
    fragmentShader = createShader(open('shaders/default.frag', 'r').read(), GL_FRAGMENT_SHADER)
    program = createPipeline([vertexShader, fragmentShader])
    glUseProgram(program)

    vao = createMesh(quadVertices, quadNormals, quadIndices)

    glViewport(0, 0, width, height)
    glClearColor(0, 0, 0, 1)

    while not glfwWindowShouldClose(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        forward = euclidean(2*math.pi * glfwGetTime(), 0)
        eye = glm.vec3(0, 0, 10)
        view = glm.lookAt(eye, eye + forward, glm.vec3(0, 1, 0))
        proj = glm.perspective(glm.radians(75), aspect, 0.1, 1000.0)
        model = glm.mat4(1)

        glUniformMatrix4fv(glGetUniformLocation(program, 'model'), 1, GL_FALSE, glm.value_ptr(model))
        glUniformMatrix4fv(glGetUniformLocation(program, 'view'), 1, GL_FALSE, glm.value_ptr(view))
        glUniformMatrix4fv(glGetUniformLocation(program, 'proj'), 1, GL_FALSE, glm.value_ptr(proj))

        glBindVertexArray(vao)
        glDrawElements(GL_TRIANGLES, len(quadIndices), GL_UNSIGNED_INT, None)

        glfwPollEvents()
        glfwSwapBuffers(window)


    glfwDestroyWindow(window)
    glfwTerminate()
