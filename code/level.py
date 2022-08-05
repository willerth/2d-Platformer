from distutils.spawn import spawn
import pygame
from tiles import *
from player import Player
from settings import *
from support import *
from particles import ParticleEffect
from enemy import *

class Level:
    def __init__(self, levelData,surface):
        #general
        self.displaySurface = surface
        self.worldShift = -4
        #terrain
        terrainLayout = importCsvLayout(levelData['terrain'])
        self.terrainSprites = self.createTileGroup(terrainLayout, 'terrain')

        playerLayout = importCsvLayout(levelData['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.playerSetup(playerLayout)

        #grass
        grassLayout = importCsvLayout(levelData['grass'])
        self.grassSprites = self.createTileGroup(grassLayout, 'grass')

        #crates
        crateLayout = importCsvLayout(levelData['crates'])
        self.crateSprites = self.createTileGroup(crateLayout, 'crates')
        
        #coins
        coinLayout = importCsvLayout(levelData['coins'])
        self.coinSprites = self.createTileGroup(coinLayout, 'coins')

        #palms
        fgPalmLayout = importCsvLayout(levelData['fg palms'])
        self.fgPalmSprites = self.createTileGroup(fgPalmLayout, 'fg palms')
        bgPalmLayout = importCsvLayout(levelData['bg palms'])
        self.bgPalmSprites = self.createTileGroup(bgPalmLayout, 'bg palms')

        #enemies
        enemyLayout = importCsvLayout(levelData['enemies'])
        self.enemySprites = self.createTileGroup(enemyLayout, 'enemies')

        #constraints
        constraintLayout = importCsvLayout(levelData['constraints'])
        self.constraintSprites = self.createTileGroup(constraintLayout, 'constraint')

        self.currentX = 0

        #dust
        self.dustSprite = pygame.sprite.GroupSingle()
        self.playerOnGround = False

    def playerSetup(self,layout):
        for rowIdx, row in enumerate(layout):
            for colIdx, val in enumerate(row):
                x = colIdx * tileSize
                y = rowIdx * tileSize
                if val == '0':
                    print('player goes here')
                if val == '1':
                    hatSurface = pygame.image.load('../graphics/character/hat.png').convert_alpha()
                    sprite = StaticTile(tileSize, x,y,hatSurface)
                    self.goal.add(sprite)


    def createTileGroup(self, layout, type):
        spriteGroup = pygame.sprite.Group()

        for rowIdx, row in enumerate(layout):
            for colIdx, val in enumerate(row):
                if val == '-1': continue
                x = colIdx * tileSize
                y = rowIdx * tileSize

                if type == 'terrain':
                    terrainTileList = importCutGraphics('../graphics/terrain/terrain_tiles.png')
                    tileSurface = terrainTileList[int(val)]
                    sprite = StaticTile(tileSize, x, y, tileSurface)
                if type == 'grass':
                    grassTileList = importCutGraphics('../graphics/decoration/grass/grass.png')
                    tileSurface = grassTileList[int(val)]
                    sprite = StaticTile(tileSize,x,y,tileSurface)
                if type == 'crates':
                    sprite = Crate(tileSize, x, y)
                if type == 'coins':
                    path = '../graphics/coins/' + ('gold' if val == '0' else 'silver')
                    sprite = Coin(tileSize, x, y, path)
                if type == 'fg palms':
                    path = '../graphics/terrain/palm_' + ('small' if val == '0' else 'large')
                    sprite = Palm(tileSize, x, y, path)
                if type == 'bg palms':
                    path = '../graphics/terrain/palm_bg'
                    sprite = Palm(tileSize,x,y,path)
                if type == 'enemies':
                    sprite = Enemy(tileSize, x, y)
                if type == 'constraint':
                    sprite = Tile(tileSize, x, y)
                spriteGroup.add(sprite)
        return spriteGroup

    def run(self):
        #background
        self.bgPalmSprites.update(self.worldShift)
        self.bgPalmSprites.draw(self.displaySurface)
        #terrain
        self.terrainSprites.update(self.worldShift)
        self.terrainSprites.draw(self.displaySurface)
        #enemies
        self.enemySprites.update(self.worldShift)
        self.constraintSprites.update(self.worldShift)
        self.enemyCollisionReverse()
        self.enemySprites.draw(self.displaySurface)
        #crates
        self.crateSprites.update(self.worldShift)
        self.crateSprites.draw(self.displaySurface)
        #grass
        self.grassSprites.update(self.worldShift)
        self.grassSprites.draw(self.displaySurface)
        #coins
        self.coinSprites.update(self.worldShift)
        self.coinSprites.draw(self.displaySurface)
        #palms
        self.fgPalmSprites.update(self.worldShift)
        self.fgPalmSprites.draw(self.displaySurface)

        #player sprites
        self.goal.update(self.worldShift)
        self.goal.draw(self.displaySurface)
        
    def enemyCollisionReverse(self):
        for enemy in self.enemySprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraintSprites, False): enemy.reverse()

'''
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
'''