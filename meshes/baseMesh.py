import numpy as np

class BaseMesh:
    def __init__(self):
        self.ctx = None
        self.program = None
        self.vboFormat = None
        self.attributes: tuple[str, ...] = None
        self.vao = None

    def getVertexData(self) -> np.array: ...

    def getVao(self):
        vertexData = self.getVertexData()
        vbo = self.ctx.buffer(vertexData)
        vao = self.ctx.vertex_array(
            self.program, [(vbo, self.vboFormat, *self.attributes)], skip_errors = True
        )
        return vao
    
    def render(self):
        self.vao.render()