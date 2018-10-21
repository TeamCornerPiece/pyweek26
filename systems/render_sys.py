import math
import glm

from pyglfw.libapi import *
from gl import *

from scripts import (
    ecs,
)

from systems.base_sys import System
from scripts.callbacks import *
from scripts.components import *


def euclidean(theta: float, phi: float):
    cosT = math.cos(theta)
    sinT = math.sin(theta)
    cosP = math.cos(phi)
    sinP = math.sin(phi)
    return glm.vec3(cosT * sinT, sinP, cosT * cosP)


class RenderSys(System):
    def init(self):
        self.callbacks = {
            CB_UPDATE: self.update,
        }

        vertexShader = createShader(open('shaders/default.vert', 'r').read(), GL_VERTEX_SHADER)
        fragmentShader = createShader(open('shaders/default.frag', 'r').read(), GL_FRAGMENT_SHADER)

        self.shader = createPipeline([vertexShader, fragmentShader])

        self.view_loc = glGetUniformLocation(self.shader, 'view')
        self.proj_loc = glGetUniformLocation(self.shader, 'proj')
        self.model_loc = glGetUniformLocation(self.shader, 'model')

    def update(self, ecs_data: ecs.ECS, dt):
        glUseProgram(self.shader)
        for cam_ent_id in ecs_data.get_entities(COMP_CAMERA, COMP_TRANSFORM):

            cam_data = ecs_data.get_component_data(cam_ent_id, COMP_CAMERA)
            forward = euclidean(2 * math.pi * glfwGetTime(), 0)
            eye = glm.vec3(0, 0, 10)
            view = glm.lookAt(eye, eye + forward, glm.vec3(0, 1, 0))
            proj = glm.perspective(cam_data[CAMERA_FOV], 1.0, 0.1, 1000.0)

            glUniformMatrix4fv(self.view_loc, 1, GL_FALSE, glm.value_ptr(view))
            glUniformMatrix4fv(self.proj_loc, 1, GL_FALSE, glm.value_ptr(proj))

            glBindVertexArray(self.engine.assets.quad_vao)
            glDrawElements(GL_TRIANGLES, self.engine.assets.len_quad_indices,
                           GL_UNSIGNED_INT, None)
