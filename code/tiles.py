import pygame
from support import importFolder

class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        #offsetY = y + size
        self.rect = self.image.get_rect(topleft = (x,y))

    def update(self, dx):
        self.rect.x += dx

#Static tiles
class StaticTile(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface

class Crate(StaticTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, pygame.image.load('../graphics/terrain/crate.png').convert_alpha())
        offsetY = y + size
        self.rect = self.image.get_rect(bottomleft = (x, offsetY))

#Animated Tiles
class AnimatedTile(Tile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = importFolder(path)
        self.animationSpeed = 0.15
        self.frameIdx = 0
        self.image = self.frames[0]
    
    def animate(self):
        self.frameIdx += 0.15
        if self.frameIdx >= len(self.frames): self.frameIdx = 0
        self.image = self.frames[int(self.frameIdx)]

    def update(self, dx):
        super().update(dx)
        self.animate()

class Coin(AnimatedTile):
    def __init__(self, size, x, y, path, value):
        super().__init__(size, x, y, path)
        self.value = value
        centerX = x + int(size/2)
        centerY = y + int(size/2)
        self.rect = self.image.get_rect(center = (centerX, centerY))

class Palm(AnimatedTile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, path)
        self.rect = self.image.get_rect(bottomleft = (x, y + size))