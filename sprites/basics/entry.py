from sprites.basics.button import Button
from conf import Conf

class Entry(Button):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = ""
        self.active = False
        self.color = Conf.ENTRY_COLOR_INACTIVE

    def update(self):
        self.text_to_image(self.text)