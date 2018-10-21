from OpenGL.GL import *

import numpy as np


class FrameBuffer(object):
    def __init__(self):
        self.fbo = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)

        self.texture = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, self.texture)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glFramebufferTexture2D(GL_FRAMEBUFFER,
                               GL_COLOR_ATTACHMENT0,
                               GL_TEXTURE_2D,
                               self.texture,
                               0)

        self.depth_buffer = glGenRenderbuffers(1)

        glBindRenderbuffer(GL_RENDERBUFFER, self.depth_buffer)

        glFramebufferRenderbuffer(GL_FRAMEBUFFER,
                                  GL_DEPTH_ATTACHMENT,
                                  GL_RENDERBUFFER,
                                  self.depth_buffer)

        # print glCheckFramebufferStatus(GL_FRAMEBUFFER)

        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def bind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)

    def unbind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def on_size(self, w, h):
        glBindTexture(GL_TEXTURE_2D, self.texture)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB8,
                     w, h, 0, GL_RGB,
                     GL_UNSIGNED_BYTE, None)

        glBindRenderbuffer(GL_RENDERBUFFER, self.depth_buffer)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, w, h)

    def __del__(self):
        if glDeleteRenderbuffers:
            glDeleteRenderbuffers(1, self.depth_buffer)
        glDeleteTextures(1, self.texture)
        glDeleteBuffers(1, self.fbo)
