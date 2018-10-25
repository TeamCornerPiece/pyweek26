from pyglfw.libapi import *
from OpenGL.GL import *

from scripts.callbacks import *

LX, LY, RX, RY, LT, RT = range(6)
A, B, X, Y, LB, RB, SELECT, START, L_STICK, R_STICK, UP, RIGHT, DOWN, LEFT = range(14)


class InputProcessor:
    def __init__(self, engine):
        self.engine = engine
        self.reset_cursor = True
        self.last_x = 0
        self.last_y = 0

        self.joy_y_sensitivity = -.4
        self.joy_x_sensitivity = .4 * 10

        # context = glfwGetCurrentContext()
        glEnable(GL_DEBUG_OUTPUT)
        glDebugMessageCallback(MessageCallback, None)

        glfwSetInputMode(engine.window, GLFW_CURSOR, GLFW_CURSOR_DISABLED)

        glfwSetKeyCallback(self.engine.window, on_key)
        glfwSetMouseButtonCallback(self.engine.window, on_mouse_button)
        glfwSetCursorEnterCallback(self.engine.window, on_cursor_enter)
        glfwSetCursorPosCallback(self.engine.window, on_cursor_pos)
        glfwSetScrollCallback(self.engine.window, on_scroll)
        glfwSetWindowSizeCallback(self.engine.window, on_window_size)
        # glfwSetDropCallback(self.window, on_file_drop)

        glfwSetWindowUserPointer(self.engine.window, self)

        self.max_joysticks = 2
        self.deadzone = .3
        self.last_joy_axis = [[0 for _ in range(6)] for _ in range(self.max_joysticks)]

    def update(self, dt: float):
        for joy_id in range(self.max_joysticks):
            if glfwJoystickPresent(joy_id):
                joy_axis = glfwGetJoystickAxes(joy_id)
                # joy_buttons = glfwGetJoystickButtons(joy_id)

                if joy_axis[LX] != self.last_joy_axis[joy_id][LX]:
                    ix = joy_axis[LX]
                    if abs(ix) < self.deadzone:
                        ix = 0
                    self.engine.dispatch(CB_PLAYER_SET_TURN, (ix, joy_id + 1))

                # if joy_axis[LY] != self.last_joy_axis[joy_id][LY]:
                #     iy = joy_axis[LY]
                #     if abs(iy) < self.deadzone:
                #         iy = 0
                #     self.engine.dispatch(CB_PLAYER_SET_TURN, (-iy * 75, joy_id + 1))

                if joy_axis[RY] != self.last_joy_axis[joy_id][RY] or joy_axis[RX] != self.last_joy_axis[joy_id][RX]:
                    self.engine.dispatch(CB_CAMERA_TURN,
                                         (joy_axis[RY] * self.joy_y_sensitivity,
                                          joy_axis[RX] * self.joy_x_sensitivity,
                                          joy_id + 1))

                if joy_axis[RT] != self.last_joy_axis[joy_id][RT]:
                    accel = joy_axis[RT] * .5 + .5
                    if accel < .2:
                        accel = 0
                    self.engine.dispatch(CB_PLAYER_SET_ACCEL, (accel, joy_id + 1))

                if joy_axis[LT] != self.last_joy_axis[joy_id][LT]:
                    reverse = joy_axis[LT] * .5 + .5
                    if reverse < .2:
                        reverse = 0
                    self.engine.dispatch(CB_PLAYER_SET_REVERSE, (reverse, joy_id + 1))

                # for button, value in enumerate(joy_buttons):
                #     if value != self.button_states[button]:
                #         self.button_states[button] = value
                #         if value:
                #             self.engine.dispatch(JOY_BUTTON_DOWN, [button])
                #         else:
                #             self.engine.dispatch(JOY_BUTTON_UP, [button])

                self.last_joy_axis[joy_id] = joy_axis

    def on_scroll(self, dx, dy):
        pass

    def on_key_down(self, key):
        if key == 265:
            self.engine.dispatch(CB_CAMERA_ZOOM, (-5, 0))
        elif key == 264:
            self.engine.dispatch(CB_CAMERA_ZOOM, (5, 0))
        elif key == 87:
            self.engine.dispatch(CB_PLAYER_SET_ACCEL, (1, 0))
        elif key == 83:
            self.engine.dispatch(CB_PLAYER_SET_REVERSE, (1, 0))
        elif key == 65:
            self.engine.dispatch(CB_PLAYER_SET_TURN, (-1, 0))
        elif key == 68:
            self.engine.dispatch(CB_PLAYER_SET_TURN, (1, 0))
        else:
            print(key)
        self.engine.dispatch(CB_KEY_DOWN, [key])

    def on_key_up(self, key):
        if key == 265:
            self.engine.dispatch(CB_CAMERA_ZOOM, (0, 0))
        elif key == 264:
            self.engine.dispatch(CB_CAMERA_ZOOM, (0, 0))
        elif key == 87:
            self.engine.dispatch(CB_PLAYER_SET_ACCEL, (0, 0))
        elif key == 83:
            self.engine.dispatch(CB_PLAYER_SET_REVERSE, (0, 0))
        elif key == 65 or key == 68:
            self.engine.dispatch(CB_PLAYER_SET_TURN, (0, 0))
        self.engine.dispatch(CB_KEY_UP, [key])

    def on_mouse_down(self, button):
        self.engine.dispatch(CB_MOUSE_DOWN, (button, self.last_x, self.last_y))

    def on_mouse_up(self, button):
        self.engine.dispatch(CB_MOUSE_UP, (button, self.last_x, self.last_y))

    def on_cursor_enter(self, entered):
        self.engine.dispatch(CB_CURSOR_ENTER, [entered])

    def on_size(self, w, h):
        self.engine.dispatch(CB_WINDOW_RESIZE, (w, h))

    def on_cursor_pos(self, x, y):
        if self.reset_cursor:
            self.reset_cursor = False
            dx = dy = 0
        else:
            dx = x - self.last_x
            dy = y - self.last_y

        dx *= 5
        dy *= 2
        self.last_x = x
        self.last_y = y

        self.engine.dispatch(CB_CAMERA_TURN, (dy, dx, 0))
        self.engine.dispatch(CB_MOUSE_MOVE, (x, y, dx, dy))


@GLFWkeyfun
def on_key(window, key, scancode, action, mods):
    if action is 1:
        glfwGetWindowUserPointer(window).on_key_down(key)

    elif action is 0:
        glfwGetWindowUserPointer(window).on_key_up(key)


@GLFWmousebuttonfun
def on_mouse_button(window, button, action, mods):
    if action is 1:
        glfwGetWindowUserPointer(window).on_mouse_down(button)
    elif action is 0:
        glfwGetWindowUserPointer(window).on_mouse_up(button)


@GLFWcursorenterfun
def on_cursor_enter(window, entered):
    glfwGetWindowUserPointer(window).on_cursor_enter(entered)


@GLFWcursorposfun
def on_cursor_pos(window, x, y):
    glfwGetWindowUserPointer(window).on_cursor_pos(x, y)


@GLFWscrollfun
def on_scroll(window, dx, dy):
    glfwGetWindowUserPointer(window).on_scroll(dx, dy)


@GLFWwindowsizefun
def on_window_size(window, w, h):
    glfwGetWindowUserPointer(window).on_size(w, h)


@GLDEBUGPROC
def MessageCallback(source, msg_type, msg_id, severity, length, message, userParam):
    print("GL CALLBACK: {} type = {}, severity = {}, message = {}".format(source, msg_type, severity,
                                                                          message.decode("utf-8")))
