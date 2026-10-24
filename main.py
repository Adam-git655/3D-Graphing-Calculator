from settings import *
from shaderClass import Shader
from scene import Scene
from player import Player
import moderngl as mgl
import pygame
import sys

from imgui_bundle import imgui
from imgui_bundle.python_backends.pygame_backend import PygameRenderer
from UIMenu import UIMenu

class Engine:
    def __init__(self):
        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 24)

        pygame.display.set_mode(WIN_RES, flags=pygame.OPENGL | pygame.DOUBLEBUF)
        self.ctx = mgl.create_context()

        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.BLEND)
        self.ctx.gc_mode = 'auto'

        self.menuMode = False

        self.clock = pygame.time.Clock()
        self.dt = 0
        self.time = 0

        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)

        self.isRunning = True
        self.onInit()

        self.setMenuMode(False)

    def onInit(self):
        self.player = Player(self)
        self.shader = Shader(self)
        self.scene = Scene(self)

        #initialize imgui
        imgui.create_context()
        imgui.get_io().display_size = pygame.display.get_surface().get_size()
        self.imguiRenderer = PygameRenderer()
        self.menu = UIMenu(self.scene)

        print("hi")

    def setMenuMode(self, enabled):
        self.menuMode = enabled
        pygame.event.set_grab(not enabled)
        pygame.mouse.set_visible(enabled)

        pygame.mouse.get_rel()

        io = imgui.get_io()
        flags = int(io.config_flags)
        noMouse = imgui.ConfigFlags_.no_mouse.value
        if enabled:
            io.config_flags = flags & ~noMouse
        else:
            io.config_flags = flags | noMouse

        
    def update(self):
        self.player.update()
        self.shader.update()
        self.scene.update()

        self.dt = self.clock.tick(60) / 1000
        self.time = pygame.time.get_ticks() * 0.001
        fps = self.clock.get_fps()
        pygame.display.set_caption(f'FPS: {fps:.0f}')

    def render(self):
        self.ctx.clear(color=BG_COLOR)
        self.scene.render()

        #render imgui
        self.imguiRenderer.process_inputs()
        imgui.new_frame()
        self.menu.draw()
        imgui.render()
        self.imguiRenderer.render(imgui.get_draw_data())

        pygame.display.flip()

    def handleEvents(self):
        for event in pygame.event.get():
            #process events in imgui windows
            self.imguiRenderer.process_event(event)

            if event.type == pygame.QUIT:
                self.isRunning = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                self.scene.showGrid = not self.scene.showGrid

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.setMenuMode(not self.menuMode)

    def run(self):
        while self.isRunning:
            self.handleEvents()
            self.update()
            self.render()
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    app = Engine()
    app.run()

