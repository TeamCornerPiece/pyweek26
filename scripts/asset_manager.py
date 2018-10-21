class AssetManager:
    '''
    Handles loading and saving assets used in the game
    '''

    def __init__(self):
        self.meshes = {}
        self.mesh_ids = {}
        self.mesh_count = 0

        self.textures = {}


