from settings import *
from meshes.baseMesh import BaseMesh

class TriangleMesh(BaseMesh):
    def __init__(self, app, triangles):
        super().__init__()

        self.app = app
        self.ctx = app.ctx
        self.program = app.shader.triangle
        self.triangles = triangles

        self.vboFormat = '3f 3f'
        self.attributes = ('in_position', 'in_color')
        self.vao = self.getVao()        

    def getVertexData(self):
        vertices = []
        colors = []

        for triangle in self.triangles:
            for point in triangle:
                vertices.append(point)
                colors.append((0.0, 1.0, 0.5))

        return np.hstack([
            np.array(vertices, dtype="float32"), 
            np.array(colors , dtype="float32")
            ])