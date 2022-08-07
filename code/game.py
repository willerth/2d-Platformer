import pygame, sys
from settings import *
from gameData import *
from level import Level
from overworld import Overworld

class Game:
    def __init__(self):
        self.maxLevel = 2
        self.overworld  = Overworld(0, self.maxLevel, screen)

    def run(self):
        self.overworld.run()

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
