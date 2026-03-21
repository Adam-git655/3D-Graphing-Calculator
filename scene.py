from settings import *
import random
from metaball import MetaBall

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

    def update(self):
        for ball in self.metaballs:
            ball.update()

    def render(self):
        for ball in self.metaballs:
            ball.render()