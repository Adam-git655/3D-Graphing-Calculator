class MetaBall:
    def __init__(self, x, y, velX, velY, radius, color):
        self.x = x
        self.y = y
        self.velX = velX
        self.velY = velY
        self.radius = radius
        self.color = color
    
    def update(self, dt):
        self.x += self.velX * dt
        self.y += self.velY * dt

    def collideWithBoundaries(self, screenWidth, screenHeight):
        if (self.x + self.radius >= screenWidth) or (self.x - self.radius <= 0):
            self.velX *= -1
        if (self.y + self.radius >= screenHeight) or (self.y - self.radius <= 0):
            self.velY *= -1