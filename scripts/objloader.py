# todo: comment


class MeshData(object):
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.vertices = []
        self.normals = []
        self.tex_coords = []
        self.indices = []


class ObjFile:
    def finish_object(self):
        if self._current_object is None:
            return

        mesh = MeshData()
        for i, point in enumerate(self.faces):
            v, tc, n = point
            mesh.indices.append(i)
            mesh.vertices.append(self.vertices[v])
            if tc == -1:
                mesh.tex_coords.append((0, 0))
            else:
                mesh.tex_coords.append(self.texcoords[tc])
            mesh.normals.append(self.normals[n])

        self.objects[self._current_object] = mesh
        # mesh.calculate_normals()
        self.faces = []

    def __init__(self, filename, swapyz=False):
        """Loads a Wavefront OBJ file. """
        self.directory = '/'.join(filename.split('/')[:-1])
        self.objects = {}
        self.lines = []
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []

        self._current_object = None

        for line in open(filename, "r"):
            if not (line.startswith('#') or line.startswith('s')):
                values = line.split()
                if values:
                    if values[0] == 'mtllib':
                        self.mtl = MTL('{}/{}'.format(self.directory, values[1]))

                    elif values[0] == 'o':
                        self.finish_object()
                        self._current_object = values[1]

                    elif values[0] == 'v':
                        v = [round(float(i), 2) for i in values[1:4]]
                        if swapyz:
                            v = v[0], v[2], v[1]
                        self.vertices.append(v)

                    elif values[0] == 'vt':
                        self.texcoords.append((float(values[1]), float(values[2])))

                    elif values[0] == 'vn':
                        v = list(map(float, values[1:4]))
                        if swapyz:
                            v = v[0], v[2], v[1]
                        self.normals.append(v)

                    elif values[0] == 'l':
                        self.lines.append([int(i) - 1 for i in values[1:]])

                    elif values[0] == 'f':
                        for v in values[1:]:
                            item = []
                            w = v.split('/')
                            item.append(int(w[0]) - 1)
                            if len(w) >= 2 and len(w[1]) > 0:
                                i = int(w[1])
                                item.append(i - 1)
                            else:
                                item.append(-1)
                            if len(w) >= 3 and len(w[2]) > 0:
                                i = int(w[2])
                                item.append(i - 1)
                            else:
                                item.append(-1)
                            self.faces.append(item)

        self.finish_object()


def MTL(filename):
    contents = {}
    mtl = None
    for line in open(filename, "r"):
        if not line.startswith('#'):
            values = line.split()
            if values:
                if values[0] == 'newmtl':
                    mtl = contents[values[1]] = {}
                elif mtl is None:
                    raise ValueError("mtl file doesn't start with newmtl stmt")
                mtl[values[0]] = values[1:]
    return contents
