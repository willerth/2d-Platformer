import pygame
from tiles import Tile
from player import Player
from settings import *
from particles import ParticleEffect

class Level:
    def __init__(self, levelData,surface):
        self.displaySurface = surface
        self.setupLevel(levelData)
        self.worldShift = 0
        self.currentX = 0

        #dust
        self.dustSprite = pygame.sprite.GroupSingle()
        self.playerOnGround = False

    def setupLevel(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        for rowIdx, row in enumerate(layout):
            for colIdx, cell in enumerate(row):
                x = tileSize * colIdx
                y = tileSize * rowIdx
                if cell == 'X':
                    tile = Tile((x,y), tileSize)
                    self.tiles.add(tile)
                #player
                if cell == 'P':
                    self.player.add(Player((x,y), self.displaySurface, self.createJumpParticles))

    def createJumpParticles(self, pos):
        if self.player.sprite.facingRight:
            pos -= pygame.math.Vector2(10,5)
        else:
            pos += pygame.math.Vector2(10, -5)
        jumpParticleSprite = ParticleEffect(pos, 'jump')
        self.dustSprite.add(jumpParticleSprite)

    def getPlayerOnGround(self):
        if self.player.sprite.onGround:
            self.playerOnGround = True
        else:
            self.playerOnGround = False

    def createLandingDust(self):
        if not self.playerOnGround and self.player.sprite.onGround and not self.dustSprite.sprites():
            if self.player.sprite.facingRight:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)
            fallDustParticle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dustSprite.add(fallDustParticle)

    def scrollX(self):
        player = self.player.sprite
        playerX = player.rect.centerx
        directionX = player.direction.x
        if playerX < screenWidth/4 and directionX < 0:
            self.worldShift = 8
            player.speed = 0
        elif playerX > screenWidth * 3/4 and directionX > 0:
            self.worldShift = -8
            player.speed = 0
        else:
            self.worldShift = 0
            player.speed = 8
    
    def horizontalMovement(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0 :
                    player.rect.left = sprite.rect.right
                    player.onLeft = True
                    self.currentX = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.onRight = True
                    self.currentX = player.rect.right

        if (player.onLeft and player.rect.left < self.currentX) or player.direction.x >= 0:
            player.onLeft = False
        if (player.onRight and player.rect.right > self.currentX) or player.direction.x <= 0:
            player.onRight = False

    def verticalMovement(self):
        player = self.player.sprite
        player.direction.y += player.gravity
        player.rect.y += player.direction.y
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y < 0:
                    player.direction.y = 0
                    player.rect.top = sprite.rect.bottom
                    player.onCeiling = True
                elif player.direction.y > 0:
                    player.direction.y = 0
                    player.rect.bottom = sprite.rect.top
                    player.onGround = True
        
        if player.onGround and (player.direction.y < 0 or player.direction.y > 1): player.onGround = False
        if player.onCeiling and (player.direction.y > 0): player.onCeiling = False

    def run(self):
        #dust
        self.dustSprite.update(self.worldShift)
        self.dustSprite.draw(self.displaySurface)

        #tiles
        self.tiles.update(self.worldShift)
        self.tiles.draw(self.displaySurface)
        self.scrollX()

        #player
        self.player.update()
        self.horizontalMovement()
        self.getPlayerOnGround()
        self.verticalMovement()
        self.createLandingDust()
        self.player.draw(self.displaySurface)
