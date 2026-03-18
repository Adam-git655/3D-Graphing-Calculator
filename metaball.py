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
        if (self.x + self.radius >= screenWidth):
            self.x = screenWidth - self.radius
            self.velX = -abs(self.velX)

        elif (self.x - self.radius <= 0):
            self.x = self.radius
            self.velX = abs(self.velX)

        if (self.y + self.radius >= screenHeight):
            self.y = screenHeight - self.radius
            self.velY = -abs(self.velY)
        elif (self.y - self.radius <= 0):
            self.y = self.radius
            self.velY = abs(self.velY)