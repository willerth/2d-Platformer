import pygame, sys
from settings import *
from level import Level
from overworld import Overworld
from ui import UI

class Game:
    def __init__(self):
        #game attributes
        self.maxLevel = 0
        self.maxHealth = 100
        self.curHealth = 100
        self.coins = 0
        #overworld
        self.overworld  = Overworld(0, self.maxLevel, screen, self.createLevel)
        self.status = 'overworld'
        #ui
        self.ui = UI(screen)

    def createLevel(self, currentLevel):
        self.level = Level(currentLevel, screen, self.createOverworld, self.changeCoins)
        self.status = 'level'

    def createOverworld(self, currentLevel, newMaxLevel):
        self.maxLevel = max(self.maxLevel, newMaxLevel)
        self.overworld = Overworld(currentLevel, self.maxLevel, screen, self.createLevel)
        self.status = 'overworld'

    def changeCoins(self, amount):
        self.coins += amount

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.ui.showHealth(self.curHealth, self.maxHealth)
            self.ui.showCoins(self.coins)

pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    game.run()

    pygame.display.update()
    clock.tick(60)
