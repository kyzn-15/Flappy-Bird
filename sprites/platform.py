import pygame
import os

from conf import Conf

class Platform():

    def __init__(self, Game):
        self.screen = Game.screen
        self.screen_rect = Game.screen_rect

        image_path = os.path.join(Conf.BASE_DIR, "assets", "land.png")
        self.image = pygame.transform.scale(pygame.image.load(image_path), (2*self.screen_rect.width, self.screen_rect.height//5))
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom

    def move(self):
        self.rect.x -= Conf.PLATFORM_SPEED
        if self.rect.centerx <= 0:
            self.rect.left = self.screen_rect.left

    def show(self):
        self.screen.blit(self.image, self.rect)