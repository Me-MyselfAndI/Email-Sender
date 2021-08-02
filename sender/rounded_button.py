from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import RoundedRectangle
from kivy.uix.button import Button


class RoundedButton(Button):
    def __init__(self, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)
        self.background_normal = "button1.png"
        self.background_down = "button2.png"
        self.border = 15, 15, 15, 15
        self.color = 0.2, 0.2, 0.2, 1