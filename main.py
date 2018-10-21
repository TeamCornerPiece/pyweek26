from pyglfw.libapi import *

if __name__ == '__main__':
    glfwInit()

    major, mintor, rev = glfwGetVersion()
    window = glfwCreateWindow(640, 480, b'Hello World!', None, None)

    while not glfwWindowShouldClose(window):


        glfwPollEvents()
        glfwSwapBuffers(window)


    glfwDestroyWindow(window)
    glfwTerminate()

