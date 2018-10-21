class InputProcessor:
    '''
    Receives input callbacks from GLFW and dispatches engine callbacks
    '''

    def __init__(self, engine):
        self.engine = engine

