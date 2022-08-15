import pygame
from gameData import levels
from support import importFolder
from decoration import Sky

class Node(pygame.sprite.Sprite):
    def __init__(self,pos,status,iconSpeed, path):
        super().__init__()
        self.frames = importFolder(path)
        self.frameIdx = 0
        self.image=self.frames[0]
        self.status = status
        self.rect = self.image.get_rect(center=pos)
        self.detectionZone = pygame.Rect(self.rect.centerx - iconSpeed/2, self.rect.centery - iconSpeed/2, iconSpeed, iconSpeed)

    def animate(self):
        self.frameIdx += 0.15
        if self.frameIdx >= len(self.frames): self.frameIdx = 0
        self.image = self.frames[int(self.frameIdx)]

    def update(self):
        self.animate()
        if not self.status == 'available':
            tintSurf = self.image.copy()
            tintSurf.fill('black', None, pygame.BLEND_RGBA_MULT)
            self.image.blit(tintSurf, (0,0))

class Icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.image.load('../graphics/overworld/hat.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)

    def update(self):
        self.rect.center = self.pos

class Overworld:
    def __init__(self, startLevel, maxLevel, surface, createLevel):
        #setup
        self.displaySurface = surface
        self.maxLevel = maxLevel
        self.currentLevel = startLevel
        self.createLevel = createLevel

        #movement logic
        self.moveDirection = pygame.math.Vector2(0,0)
        self.speed = 8
        self.moving = False

        #sprites
        self.setupNodes()
        self.setupIcon()
        self.sky = Sky(8, 'overworld')
    
    def setupNodes(self):
        self.nodes = pygame.sprite.Group()
        for index, nodeData in enumerate(levels.values()):
            if index <= self.maxLevel:
                nodeSprite = Node(nodeData['nodePos'], 'available', self.speed, nodeData['nodeGraphics'])
            else:
                nodeSprite = Node (nodeData['nodePos'], 'locked', self.speed, nodeData['nodeGraphics'])
            self.nodes.add(nodeSprite)

    def drawPaths(self):
        points = [node['nodePos'] for index, node in enumerate(levels.values()) if index <= self.maxLevel]
        if len(points) > 1:
            pygame.draw.lines(self.displaySurface, '#a04f45', False, points, 6)

    def setupIcon(self):
        self.icon = pygame.sprite.GroupSingle()
        iconSprite = Icon(self.nodes.sprites()[self.currentLevel].rect.center)
        self.icon.add(iconSprite)

    def input(self):
        if not self.moving:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT] and self.currentLevel < self.maxLevel:
                self.moveDirection = self.getMovementData(1)
                self.currentLevel += 1
                self.moving = True
            elif keys[pygame.K_LEFT] and self.currentLevel > 0:
                self.moveDirection = self.getMovementData(-1)
                self.currentLevel -= 1
                self.moving = True
            elif keys[pygame.K_SPACE]:
                self.createLevel(self.currentLevel)

    def getMovementData(self, direction):
        start = pygame.math.Vector2(self.nodes.sprites()[self.currentLevel].rect.center)
        end = pygame.math.Vector2(self.nodes.sprites()[self.currentLevel + direction].rect.center)
        return (end - start).normalize()

    def updateIconPosition(self):
        if self.moving and self.moveDirection:
            self.icon.sprite.pos += self.moveDirection * self.speed
            targetNode = self.nodes.sprites()[self.currentLevel]
            if targetNode.detectionZone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.moveDirection = pygame.math.Vector2(0,0)
            self.icon.update()
        

    def run(self):
        self.input()
        self.updateIconPosition()
        self.sky.draw(self.displaySurface)
        self.drawPaths()
        self.nodes.draw(self.displaySurface)
        self.nodes.update()

        self.icon.draw(self.displaySurface)