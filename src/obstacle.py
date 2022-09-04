import pygame 

class Block(pygame.sprite.Sprite):
    def __init__(self,blockSize,color,xPos,yPos):
        super().__init__()
        self.image = pygame.Surface((blockSize,blockSize))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = (xPos,yPos))

#Blueprint for obstacle building
shape = [
'  xxxxxxx',
' xxxxxxxxx',
'xxxxxxxxxxx',
'xxxxxxxxxxx',
'xxxxxxxxxxx',
'xxx     xxx',
'xx       xx']



