from pyglfw.libapi import *
from gl import *

from scripts.callbacks import *

from scripts import (
    input_proc,
    asset_manager,
    ecs,
)

from systems import (
    render_sys,
    physics_sys,
    level_sys,
)


class Engine:
    '''
    Runs the application
    '''

    def __init__(self):
        self.ecs_data = ecs.ECS()


        self.create_window()

        self.systems = (
            render_sys.RenderSys(self),
            level_sys.LevelSys(self),
            physics_sys.PhysicsSys(self),
        )

        self.input_proc = input_proc.InputProcessor(self)
        self.assets = asset_manager.AssetManager()

        self.dispatch(CB_LOAD_LEVEL, ['test_level'])

        self.running = True
        while self.running  and not glfwWindowShouldClose(self.window):
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            self.dispatch(CB_UPDATE, [1.0])

            glfwPollEvents()
            glfwSwapBuffers(self.window)

        glfwDestroyWindow(self.window)
        glfwTerminate()

    def create_window(self):
        glfwInit()

        major, mintor, rev = glfwGetVersion()

        width = 1280
        height = 720
        aspect = float(width) / height

        self.window = glfwCreateWindow(width, height, b'Hello World!', None, None)
        glfwMakeContextCurrent(self.window)

        glViewport(0, 0, width, height)

        glClearColor(0, 0, 0, 1)



    def dispatch(self, cb, args):
        for s in self.systems:
            if s.settings.get('active', False) and cb in s.callbacks:
                s.callbacks[cb](self.ecs_data, *args)
