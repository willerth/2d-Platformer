from ssl import SSLZeroReturnError
import pygame
from settings import *
from tiles import AnimatedTile, StaticTile
from support import *
from random import choice, randint

class Sky:
    def __init__(self, horizon, style='level'):
        self.top = pygame.image.load('../graphics/decoration/sky/sky_top.png').convert()
        self.bottom = pygame.image.load('../graphics/decoration/sky/sky_bottom.png').convert()
        self.middle = pygame.image.load('../graphics/decoration/sky/sky_middle.png').convert()
        self.horizon = horizon

        #stretch
        self.top = pygame.transform.scale(self.top, (screenWidth, tileSize))
        self.bottom = pygame.transform.scale(self.bottom, (screenWidth, tileSize))
        self.middle = pygame.transform.scale(self.middle, (screenWidth, tileSize))

        self.style = style
        if self.style == 'overworld':
            palmSurfaces = importFolder('../graphics/overworld/palms')
            self.palms = []
            for surface in [choice(palmSurfaces) for image in range(10)]:
                x = randint(0, screenWidth)
                y = (self.horizon * tileSize) + randint(50,100)
                rect = surface.get_rect(midbottom = (x,y))
                self.palms.append((surface, rect))

            cloudSurfaces = importFolder('../graphics/overworld/clouds')
            self.clouds = []
            for surface in [choice(cloudSurfaces) for image in range(8)]:
                x = randint(0, screenWidth)
                y = randint(0,self.horizon*tileSize - 100)
                rect = surface.get_rect(midbottom = (x,y))
                self.clouds.append((surface, rect))

    def draw(self, surface):
        for row in range(self.horizon):
            y = row * tileSize
            surface.blit(self.top,(0,y))
        surface.blit(self.middle, (0,self.horizon * tileSize))
        for row in range(self.horizon+1, verticalTiles):
            y = row * tileSize
            surface.blit(self.bottom,(0,y))

        if self.style == 'overworld':
            for palm in self.palms:
                surface.blit(palm[0],palm[1])
            for cloud in self.clouds:
                surface.blit(cloud[0],cloud[1])

class Water:
    def __init__(self,top,levelWidth):
        waterStart = -screenWidth
        waterTileWidth = 192
        tileXAmount = int((levelWidth + 2 * screenWidth) / waterTileWidth)
        self.waterSprites = pygame.sprite.Group()

        for tile in range(tileXAmount):
            x = tile * waterTileWidth + waterStart
            y = top
            sprite = AnimatedTile(192,x,y,'../graphics/decoration/water')
            self.waterSprites.add(sprite)
    
    def draw(self,surface,shift):
        self.waterSprites.update(shift)
        self.waterSprites.draw(surface)


class Clouds:
    def __init__(self,horizon,levelWidth,cloudNumber):
        cloudSurfList = importFolder('../graphics/decoration/clouds')
        minX = -screenWidth
        maxX = levelWidth + screenWidth
        minY = 0
        maxY = horizon
        self.cloudSprites = pygame.sprite.Group()

        for cloud in range(cloudNumber):
            cloud = choice(cloudSurfList)
            x = randint(minX, maxX)
            y = randint(minY, maxY)
            sprite = StaticTile(0,x,y,cloud)
            self.cloudSprites.add(sprite)
    
    def draw(self, surface, shift):
        self.cloudSprites.update(shift)
        self.cloudSprites.draw(surface)