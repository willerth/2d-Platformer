import pygame
from support import importFolder

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__()
        self.frameIndex = 0
        self.animationSpeed = 0.5
        if type == 'explosion':
            self.frames = importFolder('../graphics/enemy/explosion')
        else: self.frames = importFolder('../graphics/character/dust_particles/' + type)
        self.image = self.frames[int(self.frameIndex)]
        self.rect = self.image.get_rect(center = pos)
    
    def animate(self):
        self.frameIndex += self.animationSpeed
        if self.frameIndex >= len(self.frames): self.kill()
        else: self.image = self.frames[int(self.frameIndex)]

    def update(self, xShift):
        self.animate()
        self.rect.x += xShift