from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.app import App

class TextBoxSetup(BoxLayout):
    class DeleteButton(Button):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.text = " Delete "
            self.size_hint = (None, None)
            self.pos_hint = {"top": 1}
            self.height = 60
            self.width = 60

        def on_press(self, *args):
            App.get_running_app().root.ids.textbox_setups.remove_widget(self.parent)

    class FieldTitle (Label):
        def __init__(self, text, is_long=False, **kwargs):
            super().__init__(**kwargs)
            self.is_long = is_long
            self.text = "ENTER TITLE " + ("(short)" if not is_long else "(long)")
            self.background_color = (0.3, 0.3, 0.3, 1)
            self.size_hint = (1, None)
            self.height = 30
            self.bind (pos=self.update, size=self.update)
            with self.canvas.before:
                Color(rgba=self.background_color)
                self.rect = Rectangle(size=self.size, pos=self.pos)

        def update(self, *args):
            self.rect.pos = self.pos
            self.rect.size = self.size

        def on_text (self, *args):
            try:
                self.parent.text = self.text
            except Exception:
                pass

    def __init__(self, name="", is_long=False, **kwargs):
        super().__init__(**kwargs)
        self.is_long = is_long
        self.text = name
        self.delete_button = self.DeleteButton (**kwargs)
        self.field_title = self.FieldTitle (name, is_long=is_long, **kwargs)
        self.setup_label_field = TextInput (size_hint=(1, None), height=30, text="", hint_text="This field's title")
        self.setup_label_field.bind(text=self.update)

        self.spacing = 10
        self.orientation = "horizontal"
        self.size_hint = (0.5, None)
        #self.all_widgets = BoxLayout()
        self.add_widget(self.delete_button)
        self.grid_layout = GridLayout(size_hint=(0.8, 1), cols=1)
        self.grid_layout.add_widget(self.field_title)
        self.grid_layout.add_widget(self.setup_label_field)
        self.add_widget(self.grid_layout)

    #def on_parent(self, *args):
    #    App.get_running_app().root.ids.textbox_setups.add_widget(self.all_widgets)

    def update(self, *args):
        self.text = self.setup_label_field.text
        self.field_title.text = self.text
        self.field_title.text = self.text + " " + ("(short)" if not self.is_long else "(long)")
