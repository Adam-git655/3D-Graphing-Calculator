from settings import *
from meshes.baseMesh import BaseMesh

class TriangleMesh(BaseMesh):
    def __init__(self, app, triangles):
        super().__init__()

        self.app = app
        self.ctx = app.ctx
        self.program = app.shader.triangle
        self.triangles = triangles
        self.time = app.time

        self.vboFormat = '3f 3f'
        self.attributes = ('in_position', 'in_color')
        self.vao = self.getVao()        

    def getVertexData(self):
        vertices = []
        colors = []

        for triangle in self.triangles:
            for point in triangle:
                vertices.append(point)

                t = (point[1] + BOUND) / (2 * BOUND)
                r = 0.5 + 0.5 * np.sin(self.time + t * np.pi)
                g = 0.5 + 0.5 * np.sin(self.time + t * np.pi + 2.094)  # 120° offset
                b = 0.5 + 0.5 * np.sin(self.time + t * np.pi + 4.189)  # 240° offset
                colors.append((r, g, b))

        return np.hstack([
            np.array(vertices, dtype="float32"), 
            np.array(colors , dtype="float32")
            ])