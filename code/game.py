import pygame, sys
from settings import *
from gameData import *
from level import Level
from overworld import Overworld

class Game:
    def __init__(self):
        self.maxLevel = 0
        self.overworld  = Overworld(0, self.maxLevel, screen, self.createLevel)
        self.status = 'overworld'

    def createLevel(self, currentLevel):
        self.level = Level(currentLevel, screen, self.createOverworld)
        self.status = 'level'

    def createOverworld(self, currentLevel, newMaxLevel):
        self.maxLevel = max(self.maxLevel, newMaxLevel)
        self.overworld = Overworld(currentLevel, self.maxLevel, screen, self.createLevel)
        self.status = 'overworld'

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()

pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
game = Game()
#level = Level(level0, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('black')
    game.run()

    pygame.display.update()
    clock.tick(60)
