from os import walk
import pygame

def importFolder(path):
    images = []
    for _,__,imgFiles in walk(path):
        for image in imgFiles:
            fullPath = f'{path}/{image}'
            image = pygame.image.load(fullPath).convert_alpha()
            images.append(image)
    return images
