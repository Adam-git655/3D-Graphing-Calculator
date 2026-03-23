from settings import *
import random
from metaball import MetaBall
from meshes.gridMesh import GridMesh

class Scene:
    def __init__(self, app):
        self.app = app
        self.metaballs = []
        self.numMetaballs = 5

        for i in range(0, self.numMetaballs):
            pos = glm.vec3(
                    random.uniform(-1, 1),
                    random.uniform(-1, 1),
                    random.uniform(-1, 1)
                    )
            
            vel = glm.vec3(
                    random.uniform(-1, 1),
                    random.uniform(-1, 1),
                    random.uniform(-1, 1)
                    )
            
            r = random.uniform(0.3, 0.7)
            
            mb = MetaBall(app, pos.x, pos.y, pos.z, vel.x, vel.y, vel.z, r)
            self.metaballs.append(mb)

        x = np.linspace(-BOUND, BOUND, GRID_SIZE)
        y = np.linspace(-BOUND, BOUND, GRID_SIZE)
        z = np.linspace(-BOUND, BOUND, GRID_SIZE) 
        self.gridX, self.gridY, self.gridZ = np.meshgrid(x, y, z, indexing='ij')

        self.grid = GridMesh(app)

    def update(self):
        for ball in self.metaballs:
            ball.update()
        field = self.computeField()

    def render(self):
        self.grid.render()
        for ball in self.metaballs:
            ball.render()

    def computeField(self):
        field = np.zeros((GRID_SIZE, GRID_SIZE, GRID_SIZE))
        for ball in self.metaballs:
            field += ((ball.radius * ball.radius) / ((self.gridX - ball.x) + (self.gridY - ball.y) + (self.gridZ - ball.z) + 1e-5))
        return field