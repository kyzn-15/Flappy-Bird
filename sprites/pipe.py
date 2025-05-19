import pygame

from conf import Conf

class Pipe():

    def __init__(self, Game, position):
        self.screen = Game.screen
        self.screen_rect = Game.screen_rect

        self.rect = pygame.Rect(0, 0, 0.15*self.screen_rect.width, 0.4*self.screen_rect.height)
        self.head_rect = pygame.Rect(0, 0, 1.2*self.rect.width, 0.15*self.rect.height)
        self.color = Conf.PIPE_COLOR
        self.position = position

        if self.position == "top":
            self.rect.topright = self.screen_rect.topright
            self.head_rect.midbottom = self.rect.midbottom
        elif self.position == "bottom":
            self.rect.bottomright = self.screen_rect.bottomright
            self.head_rect.midtop = self.rect.midtop

    def move(self):
        self.rect.x -= Conf.PIPE_SPEED

        if self.position == "top":
            self.head_rect.midbottom = self.rect.midbottom
        elif self.position == "bottom":
            self.head_rect.midtop = self.rect.midtop

    def show(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        pygame.draw.rect(self.screen, self.color, self.head_rect)
        