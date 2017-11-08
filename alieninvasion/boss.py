import pygame
from pygame.sprite import Sprite

class Kokomon(Sprite):
    "A class to represent the single boss"

    def __init__(self,ai_settings,screen):
        Sprite.__init__(self)
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load("kokomon copy.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = 600
        self.rect.top = 0
        self.x = 600

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def stayontop(self):
        self.rect.top = 0

    def update(self):
        '''Move the boss left or right.'''
        self.x += (self.ai_settings.Kokomon_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        '''Return True if alien is at edge of screen.'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True




