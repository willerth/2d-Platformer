from os import walk
import pygame
from csv import reader 
from settings import *

def importFolder(path):
    images = []
    for _,__,imgFiles in walk(path):
        for image in imgFiles:
            fullPath = f'{path}/{image}'
            image = pygame.image.load(fullPath).convert_alpha()
            images.append(image)
    return images


def importCsvLayout(path):
    terrainMap = []
    with open(path) as map:
        level = reader(map)
        for row in level:
            terrainMap.append(list(row))
    return terrainMap

def importCutGraphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tileNumX = int(surface.get_width()/tileSize)
    tileNumY = int(surface.get_height()/tileSize)

    cutTiles = []
    for row in range(tileNumY):
        for col in range(tileNumX):
            x = col * tileSize
            y = row * tileSize
            newSurf = pygame.Surface((tileSize, tileSize))
            newSurf.blit(surface, (0,0), pygame.Rect(x,y,tileSize,tileSize))
            cutTiles.append(newSurf)
    
    return cutTiles