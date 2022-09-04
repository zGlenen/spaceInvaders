import pygame
from laser import Laser

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,screenWidth):
        super().__init__()
        self.image = pygame.image.load("graphics/player.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = 4
        self.maxWidth = screenWidth
        
        #Laser Variables
        self.ready = True
        self.laserTime = 0
        self.laserCooldownTime = 600
        self.laserSpeed = 8
        self.laser = pygame.sprite.Group()

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        
        if keys[pygame.K_SPACE]:
            if self.ready:
                self.shoot_laser()
                self.ready = False
                self.laserTime = pygame.time.get_ticks()
    
    def recharge_timer(self):
        if not self.ready:
            currentTime = pygame.time.get_ticks()
            if currentTime - self.laserTime >= self.laserCooldownTime:
                self.ready = True
        
    def screen_constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= self.maxWidth:
            self.rect.right = self.maxWidth

    def shoot_laser(self):
        self.laser.add(Laser(self.rect.center,self.laserSpeed,self.rect.bottom))
        
    def update(self):
        self.get_input()
        self.screen_constraint()
        self.recharge_timer()
        self.laser.update()