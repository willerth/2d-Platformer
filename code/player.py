from dataclasses import InitVar
from turtle import pos
import pygame
from support import importFolder
from math import sin

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,surface, createJumpParticles, changeHealth):
        super().__init__()
        self.importCharacterAssets()       
        self.frameIndex = 0
        self.animationSpeed = 0.15
        self.image = self.animations['idle'][0]
        self.rect = self.image.get_rect(topleft = pos)

        #dust particles
        self.importDustRunParticles()
        self.dustFrameIndex = 0
        self.dustAnimationSpeed = 0.15
        self.displaySurface = surface
        self.createJumpParticles = createJumpParticles

        #movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.gravity = 0.8
        self.jumpSpeed = -16

        #animation status
        self.status = 'idle'
        self.facingRight = True
        self.onGround = False
        self.onCeiling = False
        self.onLeft = False
        self.onRight = False

        #health management
        self.changeHealth = changeHealth
        self.invincible = False
        self.invincibilityDuration = 600 #ms
        self.hurtTime = 0


    def importCharacterAssets(self):
        characterPath = '../graphics/character/'
        self.animations = {'idle':[],'run':[],'jump':[],'fall':[]}
        for animation in self.animations.keys():
            fullPath = characterPath + animation
            self.animations[animation] = importFolder(fullPath)

    def importDustRunParticles(self):
        self.dustRunParticles = importFolder('../graphics/character/dust_particles/run')

    def animate(self):
        animation = self.animations[self.status]
        self.frameIndex += self.animationSpeed
        if self.frameIndex >= len(animation):
            self.frameIndex = 0
        self.image = animation[int(self.frameIndex)]
        if not self.facingRight:
            self.image = pygame.transform.flip(self.image, True, False)

        if self.invincible:
            alpha = self.waveValue()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
            
        #set rectangle
        if self.onGround:
            if self.onRight:
                self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
            elif self.onLeft:
                self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
            else:
                self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.onCeiling:
            if self.onRight:
                self.rect = self.image.get_rect(topright = self.rect.topright)
            elif self.onLeft:
                self.rect = self.image.get_rect(topleft = self.rect.topleft)
            else:
                self.rect = self.image.get_rect(midtop = self.rect.midtop)

    def animateDust(self):
        if self.status == 'run' and self.onGround:
            self.dustFrameIndex += self.dustAnimationSpeed
            if self.dustFrameIndex >= len(self.dustRunParticles):
                self.dustFrameIndex = 0

            dustParticle = self.dustRunParticles[int(self.dustFrameIndex)]

            if self.facingRight:
                pos = self.rect.bottomleft - pygame.math.Vector2(6,10)
                self.displaySurface.blit(dustParticle, pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(-6,10)
                dustParticle = pygame.transform.flip(dustParticle, True, False)
                self.displaySurface.blit(dustParticle, pos)
                
    def getInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facingRight = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facingRight = False
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.onGround:
            self.jump()

    def getStatus(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        elif self.direction.x != 0:
            self.status = 'run'
        else:
            self.status = 'idle'

    def jump(self):
        self.direction.y = self.jumpSpeed
        self.createJumpParticles(self.rect.midbottom)

    def getDamage(self):
        if not self.invincible:
            self.changeHealth(-10)
            self.invincible = True
            self.hurtTime = pygame.time.get_ticks()
            return

    def invincibilityTimer(self):
        if self.invincible:
            currentTime = pygame.time.get_ticks()
            if currentTime - self.hurtTime >= self.invincibilityDuration:
                self.invincible = False

    def waveValue(self):
        value = sin(pygame.time.get_ticks())
        return 255 if value > 0 else 0

    def update(self):
        self.getInput()
        self.getStatus()
        self.invincibilityTimer()
        self.animate()
        self.animateDust()
