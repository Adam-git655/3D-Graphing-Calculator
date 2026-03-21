from settings import *

class Camera:
    def __init__(self, position, yaw, pitch):
        self.position = glm.vec3(position)
        self.yaw = glm.radians(yaw)
        self.pitch = glm.radians(pitch)

        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)

        self.projMat = glm.perspective(V_FOV, ASPECT_RATIO, NEARPLANE, FARPLANE)
        self.viewMat = glm.mat4()

    def update(self):
        self.updateVectors()
        self.updateViewMat()

    def updateViewMat(self):
        self.viewMat = glm.lookAt(self.position, self.position + self.forward, self.up)

    def updateVectors(self):
        self.forward.x = glm.cos(self.yaw) * glm.cos(self.pitch)
        self.forward.y = glm.sin(self.pitch)
        self.forward.z = glm.sin(self.yaw) * glm.cos(self.pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def changePitch(self, deltaY):
        self.pitch -= deltaY
        self.pitch = glm.clamp(self.pitch, -PITCH_MAX, PITCH_MAX)

    def changeYaw(self, deltaX):
        self.yaw += deltaX
    
    def moveRight(self, velocity):
        self.position += self.right * velocity
    
    def moveLeft(self, velocity):
        self.position -= self.right * velocity

    def moveUp(self, velocity):
        self.position += self.up * velocity

    def moveDown(self, velocity):
        self.position -= self.up * velocity
    
    def moveForward(self, velocity):
        self.position += self.forward * velocity

    def moveBackward(self, velocity):
        self.position -= self.forward * velocity