(
    CB_UPDATE,  # dt: float
    CB_LOAD_LEVEL,  # level_name: str
    CB_SAVE_LEVEL,  # level_name: str

    CB_WINDOW_RESIZE,  # width: int, height: int
    CB_CURSOR_ENTER,
    CB_KEY_DOWN,
    CB_KEY_UP,
    CB_MOUSE_DOWN,
    CB_MOUSE_UP,
    CB_MOUSE_MOVE,
    CB_CAMERA_TURN,  # pitch: float, yaw: float, controller_id: int
    CB_CAMERA_ZOOM,  # value: float, controller_id: int

    CB_ADD_PHYSICS_ENT,  # ent_id: int
    CB_REMOVE_PHYSICS_ENT,  # ent_id: int

    CB_PLAYER_SET_REVERSE,  # value: float, controller_id: int
    CB_PLAYER_SET_ACCEL,  # value: float, controller_id: int
    CB_PLAYER_SET_TURN,  # value: float, controller_id: int

) = range(17)
