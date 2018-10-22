from pyglfw.libapi import *
from OpenGL.GL import *

from scripts.callbacks import *


class InputProcessor:
    def __init__(self, engine):
        self.engine = engine
        self.reset_cursor = True
        self.last_x = 0
        self.last_y = 0

        # context = glfwGetCurrentContext()
        glEnable(GL_DEBUG_OUTPUT)
        glDebugMessageCallback(MessageCallback, None)

        glfwSetKeyCallback(self.engine.window, on_key)
        glfwSetMouseButtonCallback(self.engine.window, on_mouse_button)
        glfwSetCursorEnterCallback(self.engine.window, on_cursor_enter)
        glfwSetCursorPosCallback(self.engine.window, on_cursor_pos)
        glfwSetScrollCallback(self.engine.window, on_scroll)
        glfwSetWindowSizeCallback(self.engine.window, on_window_size)
        # glfwSetDropCallback(self.window, on_file_drop)

        glfwSetWindowUserPointer(self.engine.window, self)

    def update(self, window):
        for joystick_id in range(1):
            if glfwJoystickPresent(joystick_id):
                joy_axis = glfwGetJoystickAxes(joystick_id)
                joy_buttons = glfwGetJoystickButtons(joystick_id)

                # ix = joy_axis[LX]
                # if abs(ix) < self.deadzone:
                #     ix = 0
                # iy = joy_axis[LY]
                # if abs(iy) < self.deadzone:
                #     iy = 0
                #
                # stopped = (ix == 0 and iy == 0)
                #
                # if not stopped or not self.joy_stopped:
                #     self.joy_stopped = stopped
                #     self.engine.dispatch(JOY_STICK, (0, ix, iy, dt))
                #
                # self.engine.dispatch(JOY_STICK, (1,
                #                                  joy_axis[RX] * -self.x_sensitivity,
                #                                  joy_axis[RY] * -self.y_sensitivity, dt))
                #
                # for button, value in enumerate(joy_buttons):
                #     if value != self.button_states[button]:
                #         self.button_states[button] = value
                #         if value:
                #             self.engine.dispatch(JOY_BUTTON_DOWN, [button])
                #         else:
                #             self.engine.dispatch(JOY_BUTTON_UP, [button])
                #
                # rt_down = joy_axis[RT] > 0
                # if rt_down != self.rt_down:
                #     self.rt_down = rt_down
                #     if self.rt_down:
                #         self.engine.dispatch(JOY_BUTTON_DOWN, [RT_BUTTON])
                #     else:
                #         self.engine.dispatch(JOY_BUTTON_UP, [RT_BUTTON])
                #
                # lt_down = joy_axis[LT] > 0
                # if lt_down != self.lt_down:
                #     self.lt_down = lt_down
                #     if self.lt_down:
                #         self.engine.dispatch(JOY_BUTTON_DOWN, [LT_BUTTON])
                #     else:
                #         self.engine.dispatch(JOY_BUTTON_UP, [LT_BUTTON])

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
            self.engine.dispatch(CB_PLAYER_SET_TURN, (1, 0))
        elif key == 68:
            self.engine.dispatch(CB_PLAYER_SET_TURN, (-1, 0))
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
