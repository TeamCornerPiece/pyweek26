from pyglfw.libapi import *

from scripts.callbacks import *

from scripts import (
    input_proc,
    asset_manager,
    ecs,
)

from systems import (
    render_sys,
)


class Engine:
    '''
    Runs the application
    '''

    def __init__(self):
        self.create_window()

        self.input_proc = input_proc.InputProcessor(self)
        self.assets = asset_manager.AssetManager()
        self.ecs_data = ecs.ECS()

        self.systems = (
            render_sys.RenderSys(self),
        )

        self.running = True
        while self.running:
            dt = 1.0

            self.dispatch(CB_UPDATE, [dt])
            print('update')

    def create_window(self):
        glfwInit()

        major, mintor, rev = glfwGetVersion()
        window = glfwCreateWindow(640, 480, b'GLFW Window', None, None)
        glfwMakeContextCurrent(window)
        
        vertexShader = createShader(open('shaders/default.vert', 'r').read(), GL_VERTEX_SHADER)
        fragmentShader = createShader(open('shaders/default.frag', 'r').read(), GL_FRAGMENT_SHADER)

        graphicsPipeline = createPipeline([vertexShader, fragmentShader])

        while not glfwWindowShouldClose(window):
            glfwPollEvents()
            glfwSwapBuffers(window)

        glfwDestroyWindow(window)
        glfwTerminate()

    def dispatch(self, cb, args):
        for s in self.systems:
            if s.settings.get('active', False) and cb in s.callbacks:
                s.callbacks[cb](self.ecs_data, *args)
