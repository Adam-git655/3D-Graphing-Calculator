from settings import *
from meshes.baseMesh import BaseMesh
import moderngl as mgl

class GridMesh(BaseMesh):
    def __init__(self, app):
        super().__init__()

        self.app = app
        self.ctx = app.ctx
        self.program = app.shader.grid

        self.vboFormat = '3f'
        self.attributes = ('in_position',)
        self.vao = self.getVao()


    def getVertexData(self):
        lines = []
        s = np.linspace(-BOUND, BOUND, GRID_SIZE)

        for y in s:
            for z in s:
                lines += [(-BOUND, y, z), (BOUND, y, z)]

        for x in s:
            for z in s:
                lines += [(x, -BOUND, z), (x, BOUND, z)]

        for x in s:
            for y in s:
                lines += [(x, y, -BOUND), (x, y, BOUND)]


        return np.array(lines, dtype="float32")
    
    def render(self):
        self.vao.render(mgl.LINES)
