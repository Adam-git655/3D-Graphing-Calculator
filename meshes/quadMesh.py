from settings import *
from meshes.baseMesh import BaseMesh

class QuadMesh(BaseMesh):
    def __init__(self, app):
        super().__init__()

        self.app = app
        self.ctx = app.ctx
        self.program = app.shader.quad

        self.vboFormat = '3f 3f'
        self.attributes = ('in_position', 'in_color')
        self.vao = self.getVao()

    def getVertexData(self):
        vertices = [
            (0.5, 0.5, 0.0), (-0.5, 0.5, 0.0), (-0.5, -0.5, 0.0),
            (0.5, 0.5, 0.0), (-0.5, -0.5, 0.0), (0.5, -0.5, 0.0)
        ]
        colors = [
            (0, 1, 0), (1, 0, 0), (1, 1, 0),
            (0, 1, 0), (1, 1, 0), (0, 0, 1)
        ]

        return np.hstack([vertices, colors], dtype="float32")
