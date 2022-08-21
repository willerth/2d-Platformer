import pygame

class UI:
    def __init__(self, surface):
        # setup
        self.displaySurface = surface

        #health
        self.healthBar = pygame.image.load('../graphics/ui/health_bar.png').convert_alpha()
        self.healthBarTopleft = (54,39)
        self.barMaxWidth = 152
        self.barHeight = 4
        #coins
        self.coin = pygame.image.load('../graphics/ui/coin.png').convert_alpha()
        self.coinRect = self.coin.get_rect(topleft = (50,61))
        self.font = pygame.font.Font('../graphics/ui/ARCADEPI.TTF', 22)

    def showHealth(self, current, full):
        self.displaySurface.blit(self.healthBar, (20,10))
        currentHealthRatio = current / full
        currentBarWidth = int(self.barMaxWidth * currentHealthRatio)
        healthBarRect = pygame.Rect(self.healthBarTopleft, (currentBarWidth, self.barHeight))
        pygame.draw.rect(self.displaySurface, '#dc4949', healthBarRect)

    def showCoins(self, amount):
        self.displaySurface.blit(self.coin, self.coinRect)
        coinAmountSurface = self.font.render(f'{amount}', False, 'black')
        coinAmountRect = coinAmountSurface.get_rect(midleft = (self.coinRect.right + 4, self.coinRect.centery))
        self.displaySurface.blit(coinAmountSurface, coinAmountRect)
