import pygame
import os

from conf import Conf

class Life():

    def __init__(self, Game):
        self.screen = Game.screen
        self.screen_rect = Game.screen_rect

        image_path = os.path.join(Conf.BASE_DIR, "assets", "life.png")
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

        self.rect.topright = self.screen_rect.topright

    def show(self):
        self.screen.blit(self.image, self.rect)