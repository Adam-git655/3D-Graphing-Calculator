# import pygame
# import random
# from metaball import MetaBall

# pygame.init()
# screen = pygame.display.set_mode((1280, 720))
# pygame.display.set_caption("Metaballs")

# clock = pygame.time.Clock()
# running = True
# dt = 0

# metaballs = []
# numMetaballs = 5

# GRID_SIZE = 10
# rows = screen.get_height() // GRID_SIZE
# cols = screen.get_width() // GRID_SIZE

# LOOKUP_TABLE = [
#     [],             #0000
#     [2, 3],         #0001
#     [1, 2],         #0010
#     [1, 3],         #0011
#     [0, 1],         #0100
#     [3, 0,  1, 2],  #0101
#     [0, 2],         #0110
#     [0, 3],         #0111
#     [0, 3],         #1000
#     [0, 2],         #1001
#     [0, 1,  2, 3],  #1010
#     [0, 1],         #1011
#     [1, 3],         #1100
#     [1, 2],         #1101
#     [2, 3],         #1110
#     [],             #1111
# ]


# def computeField():
#     field = []
#     for i in range(rows + 1):
#         field.append([])
#         for j in range(cols + 1):
#             field[i].append(0)
    
#     for i in range(rows + 1):
#         for j in range(cols + 1):
#             sampleX = j * GRID_SIZE
#             sampleY = i * GRID_SIZE

#             val = 0
#             for b in metaballs:
#                 val += (b.radius * b.radius / ((sampleX - b.x) * (sampleX - b.x) + (sampleY - b.y) * (sampleY - b.y) + 1e-5)) #avoid division by zero using 1e-5
            
#             field[i][j] = val
    
#     return field

# def marchSquares(field):
#     lineSegments = []
#     for row in range(rows):
#         for col in range(cols):
#             tl = field[row][col]
#             tr = field[row][col + 1]
#             br = field[row + 1][col + 1]
#             bl = field[row + 1][col]

#             bitIndex = ((tl > 1.0) << 3 | (tr > 1.0) << 2 | (br > 1.0) << 1 | (bl > 1.0) << 0)
#             edgePairs = LOOKUP_TABLE[bitIndex]

#             for i in range(0, len(edgePairs), 2):
#                 pos1 = estimatePoint(field, row, col, edgePairs[i])
#                 pos2 = estimatePoint(field, row, col, edgePairs[i + 1])
#                 lineSegments.append((pos1, pos2))
    
#     return lineSegments

# #estimate point on the edge using linear interpolation
# def estimatePoint(field, row, col, edge):
#     x = col * GRID_SIZE
#     y = row * GRID_SIZE

#     if edge == 0:
#         return (linearlyInterpolate(field[row][col], field[row][col + 1], x, x + GRID_SIZE) , y)
#     elif edge == 1:
#         return (x + GRID_SIZE, linearlyInterpolate(field[row][col + 1], field[row + 1][col + 1], y, y + GRID_SIZE))
#     elif edge == 2:
#         return (linearlyInterpolate(field[row + 1][col], field[row + 1][col + 1], x, x + GRID_SIZE), y + GRID_SIZE)
#     elif edge == 3:
#         return (x, linearlyInterpolate(field[row][col], field[row + 1][col], y, y + GRID_SIZE))


# def linearlyInterpolate(fieldVal1, fieldVal2, point1, point2):
#     return (point1 + (point2 - point1) * ((1 - fieldVal1)/(fieldVal2 - fieldVal1)))

# for i in range(0, numMetaballs):
#     pos = pygame.Vector2(random.randrange(100, screen.get_width() - 100), random.randrange(100, screen.get_height() - 100))
#     vel = pygame.Vector2(random.randrange(50, 300), random.randrange(50, 300))
#     r = random.randint(30, 100)
#     color = (255, 255, 255)

#     mb = MetaBall(pos.x, pos.y, vel.x, vel.y, r, color)
#     metaballs.append(mb)

# while running:
#     #event polling
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     #clear color
#     screen.fill("black")
    
#     #Update
#     for b in metaballs:
#         b.update(dt)
#         b.collideWithBoundaries(screen.get_width(), screen.get_height())  
    
#     field = computeField()
#     segments = marchSquares(field)

#     #RENDER
#     for seg in segments:
#         pygame.draw.line(screen, (0, 255, 0), seg[0], seg[1], 1)          

#     #window swap chain
#     pygame.display.flip()

#     dt = clock.tick(60) / 1000

# pygame.quit()



from settings import *
from shaderClass import Shader
from scene import Scene
from player import Player
import moderngl as mgl
import pygame
import sys

class Engine:
    def __init__(self):
        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 24)

        pygame.display.set_mode(WIN_RES, flags=pygame.OPENGL | pygame.DOUBLEBUF)
        self.ctx = mgl.create_context()

        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)
        self.ctx.gc_mode = 'auto'

        self.clock = pygame.time.Clock()
        self.dt = 0
        self.time = 0

        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)

        self.isRunning = True
        self.onInit()

    def onInit(self):
        self.player = Player(self)
        self.shader = Shader(self)
        self.scene = Scene(self)


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
        pygame.display.flip()

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False

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

