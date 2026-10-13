import pygame
from camera import Camera
from settings import *


class Player(Camera):
    def __init__(self, app, position=PLAYER_POS, yaw=-90, pitch=0):
        self.app = app
        super().__init__(position, yaw, pitch)

    def update(self):
        if not self.app.menuMode:
            self.OnInput()
            self.OnMouseCallback()
        super().update()

    def OnMouseCallback(self):
        mouseDX, mouseDY = pygame.mouse.get_rel()
        if mouseDX:
            self.changeYaw(mouseDX * MOUSE_SENSITIVITY)
        if mouseDY:
            self.changePitch(mouseDY * MOUSE_SENSITIVITY)
    
    def OnInput(self):
        key = pygame.key.get_pressed()
        vel = PLAYER_SPEED * self.app.dt
        if key[pygame.K_w]:
            self.moveForward(vel)
        if key[pygame.K_s]:
            self.moveBackward(vel)
        if key[pygame.K_a]:
            self.moveLeft(vel)
        if key[pygame.K_d]:
            self.moveRight(vel)
        if key[pygame.K_q]:
            self.moveUp(vel)
        if key[pygame.K_e]:
            self.moveDown(vel)
