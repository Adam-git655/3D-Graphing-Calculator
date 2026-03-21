from settings import *
from meshes.sphereMesh import SphereMesh

class Scene:
    def __init__(self, app):
        self.app = app
        self.sphere = SphereMesh(self.app)

    def update(self):
        modelMat = glm.mat4()
        self.app.shader.sphere['modelMat'].write(modelMat)
        
    def render(self):
        self.sphere.render()