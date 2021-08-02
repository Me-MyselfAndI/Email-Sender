from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class EntryField(BoxLayout):
    orientation = "vertical"
    allow_stretch = True
    spacing = 10
    padding = (0, 20, 0, 0)

    def __init__(self, text, width_proportion, **kwargs):
        super(EntryField, self).__init__()
        self.name = text
        self.size_hint = (width_proportion, 0.6)
        self.label = Label(text=f"Recipients' {text}s:", size_hint=(1, None), height=30, pos_hint={"center": 0.5})
        self.text_input = TextInput(multiline=True, size_hint=(1, None), height=(Window.height - 30) * 0.8)

        self.add_widget(self.label)
        self.add_widget(self.text_input)
