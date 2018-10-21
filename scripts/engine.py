from pyglfw.libapi import *

from scripts.callbacks import *

from scripts import (
    input_proc,
    asset_manager,
    ecs,
)

from systems import (
    render_sys,
    level_sys,
    physics_sys,
)


class Engine:
    '''
    Runs the application
    '''

    def __init__(self):
        # self.create_window()

        self.input_proc = input_proc.InputProcessor(self)
        self.assets = asset_manager.AssetManager()
        self.ecs_data = ecs.ECS()

        self.systems = (
            render_sys.RenderSys(self),
            level_sys.LevelSys(self),
            physics_sys.PhysicsSys(self),
        )

        self.dispatch(CB_LOAD_LEVEL, ['test_level'])


        print('starting engine')
        self.running = True
        while self.running:
            dt = 1.0

            self.dispatch(CB_UPDATE, [dt])

    def create_window(self):
        pass

    def dispatch(self, cb, args):
        for s in self.systems:
            if s.settings.get('active', False) and cb in s.callbacks:
                s.callbacks[cb](self.ecs_data, *args)
