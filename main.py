import pygame
import random
from metaball import MetaBall

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Metaballs")

clock = pygame.time.Clock()
running = True
dt = 0

metaballs = []
numMetaballs = 10

GRID_SIZE = 20
rows = screen.get_height() // GRID_SIZE
cols = screen.get_width() // GRID_SIZE


def computeField():
    field = []
    for i in range(rows):
        field.append([])
        for j in range(cols):
            field[i].append(0)
    
    for i in range(rows):
        for j in range(cols):
            sampleX = j * GRID_SIZE + (GRID_SIZE//2)
            sampleY = i * GRID_SIZE + (GRID_SIZE//2)

            val = 0
            for b in metaballs:
                val += (b.radius * b.radius / ((sampleX - b.x) * (sampleX - b.x) + (sampleY - b.y) * (sampleY - b.y) + 1e-5)) #avoid division by zero using 1e-5
            
            field[i][j] = val
    
    return field

for i in range(0, numMetaballs):
    pos = pygame.Vector2(random.randrange(100, screen.get_width() - 100), random.randrange(100, screen.get_height() - 100))
    vel = pygame.Vector2(random.randrange(50, 300), random.randrange(50, 300))
    r = random.randint(30, 100)
    color = (255, 255, 255)

    mb = MetaBall(pos.x, pos.y, vel.x, vel.y, r, color)
    metaballs.append(mb)

while running:
    #event polling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #clear color
    screen.fill("black")
    
    #Update
    for b in metaballs:
        b.update(dt)
        b.collideWithBoundaries(screen.get_width(), screen.get_height())  
    
    field = computeField()
    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)

            if field[row][col] > 1:
                pygame.draw.rect(screen, (0, 128, 0), rect)

    #RENDER
    for b in metaballs:
        pygame.draw.circle(screen, b.color, pygame.Vector2(b.x, b.y), b.radius, width = 3)   

    #window swap chain
    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()
