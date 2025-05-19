import pygame
import os

from conf import Conf

class Label:

    def __init__(self, Game, text):
        self.screen = Game.screen
        self.screen_rect = Game.screen_rect
        self.text = text

        font_path = os.path.join(Conf.BASE_DIR, "assets/fonts", Conf.FONT_FAMILY)
        self.font = pygame.font.Font(font_path, Conf.FONT_SIZE)
        self.text_image = self.font.render(self.text, True, Conf.FONT_COLOR)

        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.center = self.screen_rect.center


    def show(self):
        self.screen.blit(self.text_image, self.text_image_rect)