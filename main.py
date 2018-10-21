from pyglfw.libapi import *
from gl import *

if __name__ == '__main__':
    glfwInit()

    major, mintor, rev = glfwGetVersion()
    window = glfwCreateWindow(1280, 720, b'Hello World!', None, None)
    glfwMakeContextCurrent(window)

    vertexShader = createShader(open('shaders/default.vert', 'r').read(), GL_VERTEX_SHADER)
    fragmentShader = createShader(open('shaders/default.frag', 'r').read(), GL_FRAGMENT_SHADER)

    graphicsPipeline = createPipeline([vertexShader, fragmentShader])

    while not glfwWindowShouldClose(window):


        glfwPollEvents()
        glfwSwapBuffers(window)


    glfwDestroyWindow(window)
    glfwTerminate()
