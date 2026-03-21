from settings import *
from meshes.sphereMesh import SphereMesh

class MetaBall:
    def __init__(self, app, x, y, z, velX, velY, velZ, radius=0.5):
        self.app = app

        self.x = x
        self.y = y
        self.z = z
        self.velX = velX
        self.velY = velY
        self.velZ = velZ
        self.radius = radius

        self.sphere = SphereMesh(app, 20, 20, radius)
    
    def update(self):
        self.x += self.velX * self.app.dt
        self.y += self.velY * self.app.dt
        self.z += self.velZ * self.app.dt
        self.collideWithBoundaries(3, 3, 3)
        self.updateModelMat()

    def updateModelMat(self):
        modelMat = glm.mat4()
        modelMat = glm.translate(modelMat, glm.vec3(self.x, self.y, self.z))
        self.app.shader.sphere['modelMat'].write(modelMat)

    def collideWithBoundaries(self, boundaryWidth, boundaryHeight, boundaryDepth):
        if (self.x + self.radius >= boundaryWidth):
            self.x = boundaryWidth - self.radius
            self.velX = -abs(self.velX)

        elif (self.x - self.radius <= -boundaryWidth):
            self.x = -boundaryWidth + self.radius
            self.velX = abs(self.velX)

        if (self.y + self.radius >= boundaryHeight):
            self.y = boundaryHeight - self.radius
            self.velY = -abs(self.velY)

        elif (self.y - self.radius <= -boundaryHeight):
            self.y = -boundaryHeight + self.radius
            self.velY = abs(self.velY)

        if (self.z + self.radius >= boundaryDepth):
            self.z = boundaryDepth - self.radius
            self.velZ = -abs(self.velZ)

        elif (self.z - self.radius <= -boundaryDepth):
            self.z = -boundaryDepth + self.radius
            self.velZ = abs(self.velZ)

    def render(self):
        self.updateModelMat()
        self.sphere.render()