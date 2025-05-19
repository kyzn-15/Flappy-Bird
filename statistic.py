from database import Database

class Statistic:
    # Database instance (initialized when needed)
    _db = None
    
    # Game state flags
    intro = False
    character_selection = False  # Flag untuk halaman pemilihan karakter
    game_active = False
    play_again = True
    
    # Game statistics
    high_score = 0
    score = 0
    level = 1
    life = 3
    
    sound = 1
    
    @classmethod
    def init_database(cls):
        """Initialize the database connection if not already done"""
        if cls._db is None:
            cls._db = Database()
            # Load high score from database
            cls.high_score = cls._db.get_high_score()
    
    @classmethod
    def update_high_score(cls):
        """Update high score in memory and database if current score is higher"""
        if cls.score > cls.high_score:
            cls.high_score = cls.score
            cls.init_database()
            cls._db.save_score(cls.score)
    
    @classmethod
    def save_score(cls):
        """Save the current score to the database"""
        cls.init_database()
        cls._db.save_score(cls.score)
    
    @staticmethod
    def reset_game():
        """Reset game statistics"""
        Statistic.score = 0
        Statistic.level = 1
        Statistic.life = 3