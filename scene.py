from settings import *
from meshes.cubeMesh import CubeMesh

class Scene:
    def __init__(self, app):
        self.app = app
        self.cube = CubeMesh(self.app)

    def update(self):
        modelMat = glm.mat4()
        modelMat = glm.rotate(modelMat, self.app.time * 0.5, glm.vec3(0, 1, 0))
        modelMat = glm.rotate(modelMat, self.app.time * 0.3, glm.vec3(1, 0, 0))
        self.app.shader.cube['modelMat'].write(modelMat)

    def render(self):
        self.cube.render()