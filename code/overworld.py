import pygame
from gameData import levels

class Node(pygame.sprite.Sprite):
    def __init__(self,pos,status, iconSpeed):
        super().__init__()
        self.image=pygame.Surface((100,80))
        fillColor = 'red' if status == 'available' else 'grey'
        self.image.fill(fillColor)
        self.rect = self.image.get_rect(center=pos)
        self.detectionZone = pygame.Rect(self.rect.centerx - iconSpeed/2, self.rect.centery - iconSpeed/2, iconSpeed, iconSpeed)

class Icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.Surface((20,20))
        self.image.fill('blue')
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
    
    def setupNodes(self):
        self.nodes = pygame.sprite.Group()
        for index, nodeData in enumerate(levels.values()):
            if index <= self.maxLevel:
                nodeSprite = Node(nodeData['nodePos'], 'available', self.speed)
            else:
                nodeSprite = Node (nodeData['nodePos'], 'locked', self.speed)
            self.nodes.add(nodeSprite)

    def drawPaths(self):
        points = [node['nodePos'] for index, node in enumerate(levels.values()) if index <= self.maxLevel]
        if len(points) > 1:
            pygame.draw.lines(self.displaySurface, 'red', False, points, 6)

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
        self.drawPaths()
        self.nodes.draw(self.displaySurface)
        self.icon.draw(self.displaySurface)