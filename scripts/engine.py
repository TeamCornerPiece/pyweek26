import os
import pickle

from pyglfw.libapi import *
from gl import *

from scripts.callbacks import *
from scripts.components import *

from scripts import (
    input_proc,
    asset_manager,
    ecs,
    levels,
)

from systems import (
    render_sys,
    level_sys,
    physics_sys,
    camera_movement_sys,
    parent_sys,
    player_movement_sys,

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
            camera_movement_sys.CameraMovementSys(self),
            parent_sys.ParentSys(self),
            player_movement_sys.PlayerMovementSys(self)
        )

        self.assets = asset_manager.AssetManager()

        levels.test_level(self)
        # self.load('levels/test_level.level')

        # self.dispatch(CB_SAVE_LEVEL, ['levels/test_level.level'])
        # self.dispatch(CB_LOAD_LEVEL, ['levels/test_level.level'])
        self.dispatch(CB_WINDOW_RESIZE, [w, h])

        total_time = 0
        saved = False

        time = glfwGetTime()
        last_time = time

        while not glfwWindowShouldClose(self.window):
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            last_time = time
            time = glfwGetTime()
            dt = time - last_time

            # if total_time < 10:
            #     total_time += dt
            #     if total_time >= 10:
            #         if saved:
            #             print('load')
            #             self.dispatch(CB_LOAD_LEVEL, ['levels/test_level.level'])
            #         else:
            #             print('save')
            #             self.dispatch(CB_SAVE_LEVEL, ['levels/test_level.level'])
            #             saved = True
            #         total_time = 0

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

        self.window = glfwCreateWindow(w, h, b'GLFW Window', None, None)
        glfwMakeContextCurrent(self.window)

        glViewport(0, 0, w, h)

        glClearColor(0, 0, 0, 1)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        # glCullFace(GL_FRONT)

    def dispatch(self, cb, args=[]):
        #if cb is CB_LOAD_LEVEL:
        #    assert self.load(*args), 'failed to load {}'.format(args[0])

        for s in self.systems:
            if s.settings.get('active', False) and cb in s.callbacks:
                s.callbacks[cb](self.ecs_data, *args)

        #if cb is CB_SAVE_LEVEL:
        #    self.save(*args)

    def load(self, filename):
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                required_meshes, game_data = pickle.load(f)
                for fn in required_meshes:
                    self.assets.get_mesh_id(fn)
                self.ecs_data.set_data(game_data)

            return True

    def save(self, filename):
        with open(filename, 'wb+') as f:
            pickle.dump((self.assets.loaded_filenames,
                         self.ecs_data.data), f)
