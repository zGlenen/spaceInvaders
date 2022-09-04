import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self,pos,speed,screenHeight):
        super().__init__()
        self.laserWidth = 4
        self.laserHeight = 20
        self.image = pygame.Surface((self.laserWidth,self.laserHeight))
        self.image.fill('white')
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.maxHeight = screenHeight
        self.deathPixels = 50

    def destroy(self):
        if self.rect.y <= -(self.deathPixels) or self.rect.y >= self.maxHeight + self.deathPixels:
            self.kill()

    def update(self):
        self.rect.y -= self.speed
        self.destroy()