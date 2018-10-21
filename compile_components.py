import os

OUTFILE = 'scripts/components.py'

if os.path.exists(OUTFILE):
    os.remove(OUTFILE)


def write_line(line):
    with open(OUTFILE, 'a') as f:
        f.write(line)


COMP_SIZES = []
COMP_COUNT = 0


def add_component(name: str, args: list):
    global COMP_COUNT, COMP_SIZES
    write_line('COMP_{name} = {count}\n'.format(name=name, count=COMP_COUNT))
    i = -1
    for i, v in enumerate(args):
        write_line('{name}_{v} = {i}\n'.format(name=name, v=v, i=i + 2))
    write_line('\n')
    COMP_SIZES.append(i + 1)
    COMP_COUNT += 1


write_line('# COMPONENT CONSTANTS\n\n')

add_component('TRANSFORM', ['X', 'Y', 'Z', 'PITCH', 'YAW', 'SX', 'SY', 'SZ'])
add_component('CAMERA', ['FOV', 'NEAR', 'FAR'])
add_component('MESH', ['ID'])
add_component('INPUT', ['ID'])
add_component('PLAYER', ['ACCEL_FORCE', 'ACCEL_INPUT'])
add_component('SHAPE', ['BODY_ID', 'DX', 'DY', 'TYPE', 'MASS', 'RADIUS', 'SIZE_X', 'SIZE_Y', 'ELASTICITY', 'FRICTION'])

write_line('# SIZE INFORMATION\n\nCOMP_SIZES = {s}\nCOMP_COUNT = {c}\nENTITY = COMP_COUNT\n'.format(s=COMP_SIZES,
                                                                                                    c=COMP_COUNT))
