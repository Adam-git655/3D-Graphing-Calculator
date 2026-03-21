from settings import *
from meshes.baseMesh import BaseMesh

class CubeMesh(BaseMesh):
    def __init__(self, app):
        super().__init__()

        self.app = app
        self.ctx = app.ctx
        self.program = app.shader.cube

        self.vboFormat = '3f 3f'
        self.attributes = ('in_position', 'in_color')
        self.vao = self.getVao()

    def getVertexData(self):
        vertices = np.array([

        # front
        (-0.5, -0.5,  0.5), ( 0.5, -0.5,  0.5), ( 0.5,  0.5,  0.5),
        (-0.5, -0.5,  0.5), ( 0.5,  0.5,  0.5), (-0.5,  0.5,  0.5),
        # back
        ( 0.5, -0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5,  0.5, -0.5),
        ( 0.5, -0.5, -0.5), (-0.5,  0.5, -0.5), ( 0.5,  0.5, -0.5),
        # left
        (-0.5, -0.5, -0.5), (-0.5, -0.5,  0.5), (-0.5,  0.5,  0.5),
        (-0.5, -0.5, -0.5), (-0.5,  0.5,  0.5), (-0.5,  0.5, -0.5),
        # right
        ( 0.5, -0.5,  0.5), ( 0.5, -0.5, -0.5), ( 0.5,  0.5, -0.5),
        ( 0.5, -0.5,  0.5), ( 0.5,  0.5, -0.5), ( 0.5,  0.5,  0.5),
        # top
        (-0.5,  0.5,  0.5), ( 0.5,  0.5,  0.5), ( 0.5,  0.5, -0.5),
        (-0.5,  0.5,  0.5), ( 0.5,  0.5, -0.5), (-0.5,  0.5, -0.5),
        # bottom
        (-0.5, -0.5, -0.5), ( 0.5, -0.5, -0.5), ( 0.5, -0.5,  0.5),
        (-0.5, -0.5, -0.5), ( 0.5, -0.5,  0.5), (-0.5, -0.5,  0.5),

        ], dtype=np.float32)
        

        colors = np.array([

        *[(1.0, 0.0, 0.0)] * 6,  # front  — red
        *[(0.0, 1.0, 0.0)] * 6,  # back   — green
        *[(0.0, 0.0, 1.0)] * 6,  # left   — blue
        *[(1.0, 1.0, 0.0)] * 6,  # right  — yellow
        *[(1.0, 0.0, 1.0)] * 6,  # top    — magenta
        *[(0.0, 1.0, 1.0)] * 6,  # bottom — cyan

        ], dtype=np.float32)

        return np.hstack([vertices, colors], dtype="float32")
