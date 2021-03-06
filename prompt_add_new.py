from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from rounded_button import RoundedButton

from text_box_setup import TextBoxSetup


class PromptAddNew(BoxLayout):
    orientation = "horizontal"
    columns = 2
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.button_add_short = RoundedButton(text="Add Short Textbox", size_hint=(0.4, None), height=40)
        self.button_add_long = RoundedButton(text="Add Long Textbox", size_hint=(0.4, None), height=40)
        self.button_save = RoundedButton(text="Save Custom Fields", size_hint=(0.2, None), height=40)
        self.add_widget(self.button_add_short)
        self.add_widget(self.button_save)
        self.add_widget(self.button_add_long)

    def on_parent(self, *args):
        self.setup_page = self.parent.parent

        self.button_add_short.on_press = self.add_short_field
        self.button_add_long.on_press = self.add_long_field
        self.button_save.on_press = self.parent.parent.save_custom_fields

    def add_short_field(self):
        self.add_field(is_long=False)

    def add_long_field(self):
        self.add_field(is_long=True)

    def add_field(self, is_long=False):
        print(self.parent)
        self.setup_page.ids.textbox_setups.add_widget(TextBoxSetup(is_long=is_long))
