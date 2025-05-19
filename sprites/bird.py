import pygame
import os
from conf import Conf
from database import Database
from pokemon_api import PokemonAPI

class Bird():
    def __init__(self, Game):
        self.screen = Game.screen
        self.screen_rect = Game.screen_rect
        
        # Initialize the database and Pokemon API
        self.database = Database()
        self.pokemon_api = PokemonAPI()
        
        # Get the selected sprite from the database
        sprite_path, sprite_name = self.database.get_selected_sprite()
        
        # Load the appropriate sprite
        if sprite_path == 'bird.png':
            # Load the default bird sprite
            image_path = os.path.join(Conf.BASE_DIR, "assets", sprite_path)
            self.image = pygame.image.load(image_path)
        else:
            # Load a Pokemon sprite
            pokemon_id = sprite_path.split('.')[0]  # Remove the .png extension
            self.image = self.pokemon_api.get_pokemon_sprite(pokemon_id)
        
        self.rect = self.image.get_rect()
        
        self.fly = False
        self.pass_pipe = False
        self.angle = 0  
        
        self.rect.center = self.screen_rect.center

    def move(self):
        if self.fly:
            self.rect.y -= Conf.BIRD_FLY_SPEED
            self.angle = max(self.angle - 5, -30)  
        else:
            self.rect.y += Conf.GRAVITY
            self.angle = min(self.angle + 5, 90) 

    def show(self):
        rotated_image = pygame.transform.rotate(self.image, -self.angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        self.screen.blit(rotated_image, rotated_rect)
