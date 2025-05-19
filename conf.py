import os
import sys

class Conf:
    BASE_DIR = os.path.dirname(__file__)
    FPS = 25 
    SCREEN_SIZE = (500, 500) 
    SCREEN_BG_COLOR = (107, 52, 235)
    PLATFORM_SPEED = 5
    BIRD_FLY_SPEED = 3
    GRAVITY = 3

    PIPE_COLOR = (0, 200, 0)
    PIPE_SPEED = 5

    FONT_SIZE = 50
    FONT_COLOR = (242, 255, 0)
    
    BUTTON_FONT_SIZE = int(0.5 * FONT_SIZE)
    BUTTON_WIDTH = 90
    BUTTON_HEIGHT = 50

    ENTRY_HEIGHT = 50
    ENTRY_COLOR_ACTIVE = (255, 0, 0)
    ENTRY_COLOR_INACTIVE = (122, 255, 0)
    ENTRY_FONT_SIZE = 30
    ENTRY_FONT_COLOR = (255, 255, 255)

    @staticmethod
    def resource_path(relative_path):
        """Mendapatkan path absolut ke resource, bekerja untuk pengembangan dan executable PyInstaller"""
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    FONT_FAMILY = resource_path.__func__("assets/fonts/ka1.ttf")
    ENTRY_FONT = FONT_FAMILY
