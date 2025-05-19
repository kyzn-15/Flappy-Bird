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
        
        # Ensure there is at least a default setting for any new user upon login
        # (we'll insert lazily in Game.login)
        
        self.conn.commit()
        self.disconnect()
    
    def save_score(self, username, score):
        """Save a score to the database under given username"""
        self.connect()
        self.cursor.execute(
            'INSERT INTO scores (username, score) VALUES (?, ?)',
            (username, score)
        )
        self.conn.commit()
        self.disconnect()
    
    def get_high_score(self, username):
        """Retrieve the highest score for this username"""
        self.connect()
        self.cursor.execute(
            'SELECT MAX(score) FROM scores WHERE username = ?',
            (username,)
        )
        high_score = self.cursor.fetchone()[0]
        self.disconnect()
        return high_score if high_score is not None else 0
    
    def save_selected_sprite(self, username, sprite_path, sprite_name):
        """
        Save (or update) the selected sprite for given username.
        Uses REPLACE INTO so we don't have to delete first.
        """
        self.connect()
        self.cursor.execute('''
            REPLACE INTO player_settings (username, selected_sprite, sprite_name)
            VALUES (?, ?, ?)
        ''', (username, sprite_path, sprite_name))
        self.conn.commit()
        self.disconnect()
    
    def get_selected_sprite(self, username):
        """
        Get the currently selected sprite for given username.
        If none exists yet, returns default.
        """
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
