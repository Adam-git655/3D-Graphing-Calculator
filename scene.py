from settings import *
from meshes.cubeMesh import CubeMesh

class Scene:
    def __init__(self, app):
        self.app = app
        self.cube = CubeMesh(self.app)

    def update(self):
        pass

    def render(self):
        self.cube.render()