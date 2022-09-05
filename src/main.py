#TODO:
#Add intro screen with pic of red alien, welcome to invaders etc, press left right to move and space to shoot, you have three lives. Kill all aliens
#Add Game over screen with play again space bar
#Add High Score in center of screen
#


import pygame, sys
from player import Player
import obstacle
from alien import Alien, Mother
from random import choice, randint
from laser import Laser

class Game:
    def __init__(self):
        #Player Creation
        playerSprite = Player((screenWidth/2,screenHeight),screenWidth)
        self.player = pygame.sprite.GroupSingle(playerSprite)
        
        #Health 
        self.lives = 3
        self.liveSurf = pygame.image.load('graphics/player.png').convert_alpha()
        self.liveXStartPos = screenWidth - (self.liveSurf.get_size()[0] * 2 + 20)

        #Score
        self.score = 0
        self.font = pygame.font.Font('font/Pixeled.ttf',17)

        #Obstacle Creation
        self.shape = obstacle.shape
        self.blockSize = 6
        self.blocks = pygame.sprite.Group()
        self.obstacleAmount = 4
        self.obstacleXPos = [num * (screenWidth/self.obstacleAmount) 
                             for num in range(self.obstacleAmount)]
        sizeOfObstacle = self.blockSize*10 #10 is size of biggest line in obstacle array
        xStart = ((screenWidth/self.obstacleAmount)-sizeOfObstacle)/2 #2 is for padding on both sides of screen
        self.multiple_obtacle_creation(*self.obstacleXPos, xStart = xStart, yStart = screenHeight-120)

        #Alien Creation
        self.aliens = pygame.sprite.Group()
        self.alienLaser = pygame.sprite.Group()
        self.mother = pygame.sprite.GroupSingle()
        self.create_aliens(rows=6,cols=8,xDistance=60,yDistance=48,xOffset=70,yOffset=100)
        self.alienDirection = 1
        self.motherSpawnTime = randint(400,800)

        #Audio
        music = pygame.mixer.Sound('audio/music.wav')
        music.set_volume(0.05)
        music.play(loops = -1)
        self.laserSound = pygame.mixer.Sound('audio/laser.wav')
        self.laserSound.set_volume(0.1)
        self.explosionSound = pygame.mixer.Sound('audio/explosion.wav')
        self.explosionSound.set_volume(0.2)

#OBSTACLE METHODS
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

#ALIEN METHODS
    def create_aliens(self,rows,cols,xDistance,yDistance,xOffset,yOffset):
        for rIndex, row in enumerate(range(rows)):
            for cIndex, col in enumerate(range(cols)):
                xPos = cIndex * xDistance + xOffset
                yPos = rIndex * yDistance + yOffset

                if rIndex == 0:
                    alienSprite = Alien('red',xPos,yPos)
                elif 1<= rIndex <= 2:
                    alienSprite = Alien('green',xPos,yPos)
                else:
                    alienSprite = Alien('yellow',xPos,yPos)

                self.aliens.add(alienSprite)

    def alien_position_check(self):
        xSpeed = 1
        ySpeed = 2
        aliens = self.aliens.sprites()
        if aliens:
            for alien in aliens:
                if alien.rect.left == 0:
                    self.alienDirection = xSpeed
                    self.alien_move_down(ySpeed)
                elif alien.rect.right == screenWidth:
                    self.alienDirection = -(xSpeed)
                    self.alien_move_down(ySpeed)
    
    def alien_move_down(self,distance):
        for alien in self.aliens.sprites():
            alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            speedDifficulty = randint(5,8)
            alien = choice(self.aliens.sprites())
            laser = Laser(alien.rect.center,-(speedDifficulty),screenHeight)
            self.alienLaser.add(laser)
            self.laserSound.play()

    def alien_mother_timer(self):
        self.motherSpawnTime -= 1
        if self.motherSpawnTime <= 0:
            self.mother.add(Mother(choice(['right','left']),screenWidth))
            self.motherSpawnTime = randint(400,800)

#GAME METHODS   
    def collision_checks(self):
        if self.player.sprite.laser:
            for laser in self.player.sprite.laser:
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()
                
                aliensHit = pygame.sprite.spritecollide(laser,self.aliens,True)
                if aliensHit:
                    for alien in aliensHit:
                        self.score += alien.value
                        laser.kill()
                        self.explosionSound.play()

                if pygame.sprite.spritecollide(laser,self.mother,True):
                    self.score += 500
                    laser.kill()

        if self.alienLaser:
            for laser in self.alienLaser:
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()
                if pygame.sprite.spritecollide(laser,self.player,False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()

        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien,self.blocks,True)

                if pygame.sprite.spritecollide(alien,self.player,False):
                    print('GAME OVER')

    def display_lives(self):
        for life in range(self.lives - 1):
            offset = 10
            xPos = self.liveXStartPos + (life * (self.liveSurf.get_size()[0] + offset))
            yPos = 8
            screen.blit(self.liveSurf,(xPos,yPos))

    def display_score(self):
        scoreSurface = self.font.render(f'Score: {self.score}',False,('white'))
        scoreRect = scoreSurface.get_rect(topleft = (10,-5))
        screen.blit(scoreSurface,scoreRect)

    def victory_message(self):
        if not self.aliens.sprites():
            victorySurf = self.font.render('WINNER',False,'white')
            victoryRect = victorySurf.get_rect(center = (screenWidth/2,screenHeight,2))
            screen.blit(victorySurf,victoryRect)

    def run(self):
        self.player.update()
        self.aliens.update(self.alienDirection)
        self.alienLaser.update()
        self.alien_mother_timer()
        self.mother.update()

        self.alien_position_check()
        self.collision_checks()
        
        self.alienLaser.draw(screen)
        self.player.draw(screen)
        self.player.sprite.laser.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.mother.draw(screen)
        self.display_lives()
        self.display_score()
        self.victory_message()

class CRT:
    def __init__(self):
        self.tv = pygame.image.load('graphics/tv.png').convert_alpha()
        self.tv = pygame.transform.scale(self.tv,(screenWidth,screenHeight))

    def create_crt_lines(self):
        lineHeight = 3
        lineAmount = int(screenHeight / lineHeight)
        for line in range(lineAmount):
            yPos = line * lineHeight
            pygame.draw.line(self.tv,'dark grey',(0,yPos),(screenWidth,yPos),1)

    def draw(self):
        self.tv.set_alpha(randint(85,100))
        self.create_crt_lines()
        screen.blit(self.tv,(0,0))

if __name__ == '__main__':  
    pygame.init()
    screenWidth = 600
    screenHeight = 600
    screen = pygame.display.set_mode((screenWidth,screenHeight))
    clock = pygame.time.Clock()
    game = Game()
    crt = CRT()

    laserDifficulty = 800
    alienLaser = pygame.USEREVENT + 1
    pygame.time.set_timer(alienLaser,laserDifficulty)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == alienLaser:
                game.alien_shoot()

        screen.fill((30,30,30))
        game.run()
        crt.draw()

        pygame.display.flip()
        clock.tick(60)