import pygame
from tiles import *
from player import Player
from settings import *
from support import *
from particles import ParticleEffect
from enemy import *
from decoration import *
from gameData import levels



class Level:
    def __init__(self, currentLevel, surface, createOverworld, changeCoins, changeHealth):
        #general
        self.displaySurface = surface
        self.worldShift = 0
        self.currentX = 0

        #overworld connection
        self.createOverworld = createOverworld
        self.currentLevel = currentLevel
        levelData = levels[currentLevel]
        self.newMaxLevel = levelData['unlock']
        #terrain
        terrainLayout = importCsvLayout(levelData['terrain'])
        self.terrainSprites = self.createTileGroup(terrainLayout, 'terrain')

        #player
        playerLayout = importCsvLayout(levelData['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.playerSetup(playerLayout, changeHealth)

        #ui
        self.changeCoins = changeCoins

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

        #decoration
        self.sky = Sky(8)
        self.levelWidth = len(terrainLayout[0]) * tileSize
        self.water = Water(screenHeight - 15, self.levelWidth)
        self.clouds = Clouds(6,self.levelWidth,20)

        #dust
        self.dustSprite = pygame.sprite.GroupSingle()
        self.playerOnGround = False

        #explosion particles
        self.explosionSprites = pygame.sprite.Group()

    def playerSetup(self,layout, changeHealth):
        for rowIdx, row in enumerate(layout):
            for colIdx, val in enumerate(row):
                x = colIdx * tileSize
                y = rowIdx * tileSize
                if val == '0':
                    sprite = Player((x,y),self.displaySurface, self.createJumpParticles, changeHealth)
                    self.player.add(sprite)
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
                    value = 5 if val == '0' else 1
                    sprite = Coin(tileSize, x, y, path, value)
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
      
    def enemyCollisionReverse(self):
        for enemy in self.enemySprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraintSprites, False): enemy.reverse()

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
        if playerX < screenWidth/3 and directionX < 0:
            self.worldShift = 8
            player.speed = 0
        elif playerX > screenWidth * 2/3 and directionX > 0:
            self.worldShift = -8
            player.speed = 0
        else:
            self.worldShift = 0
            player.speed = 8
    
    def horizontalMovement(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        collidableSprites = self.terrainSprites.sprites() + self.fgPalmSprites.sprites() + self.crateSprites.sprites()
        for sprite in collidableSprites:
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
        collidableSprites = self.terrainSprites.sprites() + self.fgPalmSprites.sprites() + self.crateSprites.sprites()
        for sprite in collidableSprites:
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

    def checkDeath(self):
        if self.player.sprite.rect.top > screenHeight:
            self.createOverworld(self.currentLevel, self.currentLevel)

    def checkWin(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.createOverworld(self.currentLevel, self.newMaxLevel)

    def checkCoinCollisions(self):
        collidedCoins = pygame.sprite.spritecollide(self.player.sprite, self.coinSprites, True)
        if collidedCoins:
            for coin in collidedCoins:
                self.changeCoins(coin.value)

    def checkEnemyCollisions(self):
        enemyCollisions = pygame.sprite.spritecollide(self.player.sprite, self.enemySprites, False)
        if enemyCollisions:
            for enemy in enemyCollisions:
                enemyCenter = enemy.rect.centery
                enemyTop = enemy.rect.top
                playerBottom = self.player.sprite.rect.bottom
                if enemyTop < playerBottom < enemyCenter and self.player.sprite.direction.y >= 0:
                    enemy.kill()
                    self.player.sprite.direction.y = self.player.sprite.jumpSpeed
                    explosionSprite = ParticleEffect(enemy.rect.center, 'explosion')
                    self.explosionSprites.add(explosionSprite)
                else:
                    self.player.sprite.getDamage()

    def run(self):
        #decoration
        self.sky.draw(self.displaySurface)
        self.clouds.draw(self.displaySurface, self.worldShift)
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
        self.checkEnemyCollisions()
        self.enemySprites.draw(self.displaySurface)
        self.explosionSprites.update(self.worldShift)
        self.explosionSprites.draw(self.displaySurface)
        #crates
        self.crateSprites.update(self.worldShift)
        self.crateSprites.draw(self.displaySurface)
        #grass
        self.grassSprites.update(self.worldShift)
        self.grassSprites.draw(self.displaySurface)
        #coins
        self.coinSprites.update(self.worldShift)
        self.coinSprites.draw(self.displaySurface)
        self.checkCoinCollisions()
        #palms
        self.fgPalmSprites.update(self.worldShift)
        self.fgPalmSprites.draw(self.displaySurface)

        #player sprites
        self.player.update()
        self.horizontalMovement()
        self.getPlayerOnGround()
        self.verticalMovement()
        self.createLandingDust()
        self.scrollX()
        self.dustSprite.update(self.worldShift)
        self.dustSprite.draw(self.displaySurface)
        self.player.draw(self.displaySurface)
        self.goal.update(self.worldShift)
        self.goal.draw(self.displaySurface)

        self.checkDeath()
        self.checkWin()
        #water
        self.water.draw(self.displaySurface, self.worldShift)

