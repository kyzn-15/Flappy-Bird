## main.py
import pygame
import sys
import os
from random import choice

from conf import Conf
from statistic import Statistic
from database import Database
from sprites.platform import Platform
from sprites.bird import Bird
from sprites.pipe import Pipe
from sprites.sprite_selector import SpriteSelector

from sprites.basics.label import Label
from sprites.basics.button import PlayButton, Button
from sprites.basics.entry import Entry

class Game:
    pygame.init()
    screen = pygame.display.set_mode(Conf.SCREEN_SIZE)
    screen_rect = screen.get_rect()

    def __init__(self):
        # Initialize database and user
        self.database = Database()
        self.username = None  # set after login via Entry

        self.font = pygame.font.Font(None, 26)
        self.game_title_label = Label(self, "Flappy Bird")
        self.login_button = Button(self, "LOGIN")
        self.play_button = Button(self, "PLAY NOW")
        self.play_again_button = Button(self, "PLAY AGAIN")
        self.exit_button = Button(self, "EXIT")
        self.mute_button = Button(self, "MUTE")

        # Init CHANGE CHARACTER BUTTON
        self.character_button = Button(self, "CHANGE POKEMON SKIN")
        self.character_button.rect.center = (self.screen_rect.centerx, self.screen_rect.centery + 30)
        self.character_button.text_image_rect.center = self.character_button.rect.center

        # Mute button fixed top-left
        self.mute_button.rect.topleft = (10, 10)

        # Center play button
        self.play_button.rect.center = (self.screen_rect.centerx,
                                        self.screen_rect.centery - 30)
        self.play_button.text_image_rect.center = self.play_button.rect.center

        # Play again & exit layout
        self.reposition_play_again_and_exit_button()

        # Sprites & selector
        self.platform = Platform(self)
        self.bird = Bird(self)
        self.pipes = [Pipe(self, pos) for pos in ["top", "bottom"]]
        self.sprite_selector = SpriteSelector(self)

        # DB & sound
        Statistic.init_database()
        self.is_muted = False
        self.play_backsound("theme.wav")
        Statistic.intro = False

        # Blink effect
        self.blink_counter = 0
        self.blink_state = True

    def reposition_play_again_and_exit_button(self):
        # Place PLAY AGAIN button below the play button
        self.play_again_button.rect.center = (self.screen_rect.centerx, self.screen_rect.centery + 80)
        self.play_again_button.text_image_rect.center = self.play_again_button.rect.center
        # Place EXIT button below the PLAY AGAIN button
        self.exit_button.rect.center = (self.screen_rect.centerx, self.screen_rect.centery + 140)
        self.exit_button.text_image_rect.center = self.exit_button.rect.center

    def loop(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.screen.fill((0, 0, 0))  # Clear screen with black, or use Conf.SCREEN_BG_COLOR
            # Draw your game objects here, e.g.:
            # self.platform.show()
            # self.bird.show()
            # self.pipes[0].show()
            # self.pipes[1].show()
            pygame.display.flip()
            clock.tick(Conf.FPS)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.loop()


## database.py
import sqlite3
import os
from conf import Conf

class Database:
    def __init__(self):
        self.db_path = os.path.join(Conf.BASE_DIR, 'flappy_bird.db')
        self.conn = None
        self.cursor = None
        self.initialize_db()

    def connect(self):
        """Connect to the SQLite database"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def initialize_db(self):
        """Create the scores and player_settings tables if they don't exist"""
        self.connect()
        # Create scores table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            score INTEGER NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        # Create player_settings table for character selection
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS player_settings (
            username TEXT PRIMARY KEY,
            selected_sprite TEXT NOT NULL,
            sprite_name TEXT NOT NULL
        )
        ''')
        self.conn.commit()
        self.disconnect()

    def save_score(self, username, score):
        self.connect()
        self.cursor.execute(
            'INSERT INTO scores (username, score) VALUES (?, ?)',
            (username, score)
        )
        self.conn.commit()
        self.disconnect()

    def get_high_score(self, username):
        self.connect()
        self.cursor.execute(
            'SELECT MAX(score) FROM scores WHERE username = ?',
            (username,)
        )
        high_score = self.cursor.fetchone()[0]
        self.disconnect()
        return high_score if high_score is not None else 0

    def save_selected_sprite(self, username, sprite_path, sprite_name):
        self.connect()
        self.cursor.execute('''
            REPLACE INTO player_settings (username, selected_sprite, sprite_name)
            VALUES (?, ?, ?)
        ''', (username, sprite_path, sprite_name))
        self.conn.commit()
        self.disconnect()

    def get_selected_sprite(self, username=None):
        """
        Get the currently selected sprite for given username.
        If none exists yet or no username provided, returns default.
        """
        if username is None:
            username = 'guest'
        self.connect()
        self.cursor.execute(
            'SELECT selected_sprite, sprite_name FROM player_settings WHERE username = ?',
            (username,)
        )
        row = self.cursor.fetchone()
        self.disconnect()
        if row:
            return row[0], row[1]
        else:
            # default values
            return 'bird.png', 'Flappy Bird'


## sprites/bird.py
import pygame
import os
from conf import Conf
from database import Database

class Bird(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.database = Database()

        # fetch sprite based on (optional) username
        sprite_path, sprite_name = self.database.get_selected_sprite(game.username)
        full_path = os.path.join(Conf.BASE_DIR, "assets/img", sprite_path)
        self.image = pygame.image.load(full_path).convert_alpha()
        self.name = sprite_name
        
        # initialize position, physics, etc.
        self.rect = self.image.get_rect(center=game.screen_rect.center)
        self.fly = False
        self.pass_pipe = False
        self.velocity = 0
