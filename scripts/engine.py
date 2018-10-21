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

        w = 1280
        h = 720

        self.ecs_data = ecs.ECS()

        self.create_window(w, h)
        self.input_proc = input_proc.InputProcessor(self)

        self.systems = (
            render_sys.RenderSys(self),
            level_sys.LevelSys(self),
            physics_sys.PhysicsSys(self),
        )

        self.assets = asset_manager.AssetManager()

        self.dispatch(CB_LOAD_LEVEL, ['test_level'])
        self.dispatch(CB_WINDOW_RESIZE, [w, h])

        self.running = True
        while self.running  and not glfwWindowShouldClose(self.window):
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            dt = 1.0

            self.input_proc.update(dt)
            self.dispatch(CB_UPDATE, [dt])

            glfwPollEvents()
            glfwSwapBuffers(self.window)

        glfwDestroyWindow(self.window)
        glfwTerminate()

    def create_window(self, w, h):
        glfwInit()

        major, mintor, rev = glfwGetVersion()


        aspect = float(w) / h

        self.window = glfwCreateWindow(w, h, b'Hello World!', None, None)
        glfwMakeContextCurrent(self.window)

        glViewport(0, 0, w, h)

        glClearColor(0, 0, 0, 1)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        # glCullFace(GL_FRONT)


    def dispatch(self, cb, args):
        for s in self.systems:
            if s.settings.get('active', False) and cb in s.callbacks:
                s.callbacks[cb](self.ecs_data, *args)
