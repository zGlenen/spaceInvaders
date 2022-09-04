import pygame, sys
from player import Player
import obstacle

class Game:
    def __init__(self):
        #Player Creation
        playerSprite = Player((screenWidth/2,screenHeight),screenWidth)
        self.player = pygame.sprite.GroupSingle(playerSprite)

        #Obstacle Creation
        self.shape = obstacle.shape
        self.blockSize = 6
        self.blocks = pygame.sprite.Group()
        self.obstacleAmount = 4
        self.obstacleXPos = [num * (screenWidth/self.obstacleAmount) 
                             for num in range(self.obstacleAmount)]
        self.multiple_obtacle_creation(*self.obstacleXPos, xStart = screenWidth/15, yStart = 480)

# obstacle size = blocksize * size of obstacle = 10 (60)
#screen width - obstaclesize * obstacleamount 600 - 240 = 360
#360 / obstacleamount +1 = 360/5 = 72

    def create_obstacle(self, xStart, yStart, offsetX):
        color = (241,79,80)

        for rIndex, row in enumerate(self.shape):
            for cIndex, col in enumerate(row):
                if col == 'x':
                    xPos = xStart + cIndex * self.blockSize + offsetX
                    yPos = yStart +rIndex * self.blockSize
                    block = obstacle.Block(self.blockSize,color,xPos,yPos)
                    self.blocks.add(block)

    def multiple_obtacle_creation(self,*offset,xStart,yStart):
        for offsetX in offset:
            self.create_obstacle(xStart,yStart,offsetX)

    def run(self):
        self.player.update()
        self.player.draw(screen)
        self.player.sprite.laser.draw(screen)
        self.blocks.draw(screen)

if __name__ == '__main__':  
    pygame.init()
    screenWidth = 600
    screenHeight = 600
    screen = pygame.display.set_mode((screenWidth,screenHeight))
    clock = pygame.time.Clock()
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((30,30,30))
        game.run()

        pygame.display.flip()
        clock.tick(60)