from PIL import Image
from OpenGL.GL import *
import numpy as np

import glm

from freetype import *


def finish(linear):
    glGenerateMipmap(GL_TEXTURE_2D)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    if linear:
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    else:
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)


def load_texture(fn, linear=True):
    tex_id = glGenTextures(1)

    image = Image.open(fn)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)

    data = np.array(list(image.getdata()), np.uint8)

    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glBindTexture(GL_TEXTURE_2D, tex_id)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB8,
                 image.width, image.height, 0, GL_RGB,
                 GL_UNSIGNED_BYTE, data)

    image.close()

    finish(linear)

    return tex_id, image.width, image.height


def from_string(string, linear=False):
    tex_id = glGenTextures(1)

    face = Face('./Vera.ttf')
    face.set_char_size(32 * 48)

    try:
        buffer = rasterizeString(face, string)
    except:
        buffer = rasterizeString(face, 'didnt work')

    buffer = np.flip(buffer, 0)

    # image = Image.fromarray(buffer)
    # image.show()
    # image = image.transpose(Image.FLIP_TOP_BOTTOM)

    # data = np.array(list(image.getdata()), np.uint8)

    glBindTexture(GL_TEXTURE_2D, tex_id)

    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_ALPHA8,
                 buffer.shape[1], buffer.shape[0], 0, GL_ALPHA,
                 GL_UNSIGNED_BYTE, buffer.flatten())


    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    # image.close()

    # finish(linear)

    return tex_id, glm.vec2(buffer.shape[::-1])


def rasterizeString(face, string):
    slot = face.glyph

    # Loop over characters to determine bounding box
    width, height, baseline = 0, 0, 0
    for i in range(len(string)):
        prev, curr = '\0' if i is 0 else string[i - 1], string[i]

        face.load_char(curr)
        bitmap = slot.bitmap

        height = max(height, bitmap.rows + max(0, -(slot.bitmap_top - bitmap.rows)))
        baseline = max(baseline, max(0, -(slot.bitmap_top - bitmap.rows)))

        kerning = face.get_kerning(prev, curr)

        width += (slot.advance.x >> 6) + (kerning.x >> 6)

    # Rasterize the string
    buffer = np.zeros((height, width), dtype=np.ubyte)
    x, y = 0, 0
    for i in range(len(string)):
        prev, curr = '\0' if i is 0 else string[i - 1], string[i]

        face.load_char(curr)
        bitmap = slot.bitmap

        top = slot.bitmap_top
        left = slot.bitmap_left
        w, h = bitmap.width, bitmap.rows
        y = height - baseline - top

        kerning = face.get_kerning(prev, curr)
        x += (kerning.x >> 6)
        buffer[y:y + h, x:x + w] += np.array(bitmap.buffer, dtype='ubyte').reshape(h, w)
        x += (slot.advance.x >> 6)

    return buffer
