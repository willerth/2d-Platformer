import pygame, sys
from settings import *
from gameData import *
from level import Level

pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()

level = Level(level0, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('grey')
    level.run()

    pygame.display.update()
    clock.tick(60)
