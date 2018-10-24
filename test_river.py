import pygame
import glm

CANVAS = pygame.display.set_mode((1500, 800))

CLOCK = pygame.time.Clock()

ponds = []
rivers = []

finished = []

offset = glm.vec2()
selection_id = 0
clicks = []
dragging = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                pass
                # if rivers:
                #     with open('river_nodes.py', 'w') as f:
                #         f.write('import glm\n\nnodes = [\n')
                #         center = nodes[0][0]
                #         for i, (pos, extent) in enumerate(nodes):
                #             vec_str = '(glm.vec3({pos.x}, {y}, {pos.y}), glm.vec3({extent.x}, 0, {extent.y})),\n'
                #             f.write(vec_str.format(pos=(pos - center) * .2,
                #                                    y=-i,
                #                                    extent=extent * .2))
                #         f.write(']\n')
                #     print('saved')
            elif event.key == pygame.K_SPACE:
                if clicks:
                    if len(clicks) == 1:
                        if selection_id not in finished:
                            click = clicks[0]

                            min_dist = 10000
                            closest_node = None
                            for pond in ponds:
                                for i, node in enumerate(pond):
                                    prev_node = pond[i - 1]
                                    midpoint = (node + prev_node) * .5
                                    dist = glm.length(click - midpoint)
                                    if dist < min_dist:
                                        min_dist = dist
                                        closest_node = midpoint, node - midpoint

                            if closest_node and min_dist < 50:
                                if selection_id < len(rivers):
                                    finished.append(selection_id)
                                else:
                                    rivers.append([])
                                rivers[selection_id].append(closest_node)

                    elif len(clicks) == 2:
                        if selection_id not in finished:
                            if selection_id < len(rivers):
                                rivers[selection_id].append((clicks[0], clicks[1] - clicks[0]))

                    else:
                        ponds.append(clicks)

                    clicks = []

            elif event.key == pygame.K_BACKSPACE:
                clicks = []

            elif event.key == pygame.K_UP:
                selection_id = min(len(rivers), selection_id + 1)

            elif event.key == pygame.K_DOWN:
                selection_id = max(0, selection_id - 1)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clicks.append(glm.vec2(event.pos) - offset)
            elif event.button == 3:
                dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                offset.x += event.rel[0]
                offset.y += event.rel[1]

    CANVAS.fill((0, 0, 0))

    for river_id, nodes in enumerate(rivers):
        if river_id == selection_id:
            color = (0, 255, 0)
        else:
            color = (0, 0, 255)

        for node_id, (pos, edge) in enumerate(nodes[:-1]):
            next_pos, next_edge = nodes[node_id + 1]
            # for i in (-1, 1):
            #     start = pos + edge * i
            #     end = next_pos + next_edge * i
            #     pygame.draw.line(CANVAS, (0, 0, 255), start, end, 2)

            a = pos - edge
            b = pos + edge
            c = next_pos - next_edge
            pygame.draw.polygon(CANVAS, color, (a + offset, b + offset, c + offset), 2)

            a = next_pos - next_edge
            b = next_pos + next_edge
            c = pos + edge
            pygame.draw.polygon(CANVAS, color, (a + offset, b + offset, c + offset), 2)

    for pond_id, points in enumerate(ponds):
        pygame.draw.polygon(CANVAS, (0, 0, 127), [p + offset for p in points], 2)

    if selection_id < len(rivers):
        for pos, extents in rivers[selection_id]:
            pygame.draw.circle(CANVAS, (255, 0, 0),
                               (int(pos.x + offset.x), int(pos.y + offset.y)), 5)

    for pos in clicks:
        pygame.draw.circle(CANVAS, (0, 255, 0),
                           (int(pos.x + offset.x), int(pos.y + offset.y)), 3)

    pygame.display.flip()
