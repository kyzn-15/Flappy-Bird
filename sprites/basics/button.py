import pygame
import os

from conf import Conf

class PlayButton:

    def __init__(self, Game):
        self.screen = Game.screen
        self.screen_rect = Game.screen_rect

        image_path = os.path.join(Conf.BASE_DIR, "assets", "play.png")
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

        self.image = pygame.transform.scale(self.image, (self.rect.width//10, self.rect.height//10))
        self.rect = self.image.get_rect()

        self.rect.center = self.screen_rect.center
        self.rect.y += 100

    def show(self):
        self.screen.blit(self.image, self.rect)

class Button:

    def __init__(self, Game, text):
        self.screen = Game.screen
        self.screen_rect = Game.screen_rect

        width = (len(text) - 4) * Conf.BUTTON_FONT_SIZE//1.5
        self.rect = pygame.Rect(0,0, Conf.BUTTON_WIDTH + width, Conf.BUTTON_HEIGHT)
        self.font_path = os.path.join(Conf.BASE_DIR, "assets/fonts", Conf.FONT_FAMILY)
        self.color = (255, 0, 0)
        self.text_to_image(text)

    def text_to_image(self, text):

        self.font = pygame.font.Font(self.font_path, Conf.BUTTON_FONT_SIZE)
        self.text_image = self.font.render(text, True, Conf.FONT_COLOR)

        self.text_image_rect = self.text_image.get_rect()

        self.rect.center = self.screen_rect.center
        self.rect.y += 100
        self.text_image_rect.center = self.rect.center
        self.text_image_rect.y += 8

    def show(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        self.screen.blit(self.text_image, self.text_image_rect)

    