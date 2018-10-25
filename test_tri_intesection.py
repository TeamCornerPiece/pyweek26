import pygame
import glm

CANVAS = pygame.display.set_mode((1500, 800))

CLOCK = pygame.time.Clock()

A = glm.vec2(100, 100)
B = glm.vec2(300, 200)
C = glm.vec2(100, 300)
P = glm.vec2(0, 0)


def cross(a, b):
    return glm.dot(a, glm.vec2(-b.y, b.x))


def tri_intersection(p, a, b, c):
    sign = cross(p - a, b - a) > 0
    return (cross(p - b, c - b) > 0) == sign and (cross(p - c, a - c) > 0) == sign


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEMOTION:
            P.x = event.pos[0]
            P.y = event.pos[1]

    CANVAS.fill((0, 0, 0))

    if tri_intersection(P, A, B, C):
        color = (0, 255, 0)
    else:
        color = (255, 0, 0)

    pygame.draw.circle(CANVAS, color, list(map(int, P)), 10)

    pygame.draw.polygon(CANVAS, (0, 0, 255), (A, B, C), 2)

    pygame.display.flip()
