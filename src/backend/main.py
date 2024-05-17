from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty


class MainScreen(BoxLayout):
    user_name = StringProperty("Guest")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #print(f"MainScreen instance created: {self}")

    def set_user(self, username):
        self.user_name = username
        #print(f"Username set to: {self.user_name}")

    def on_user_name(self, instance, value):
        print(f"User name changed to: {value}")
        if self.ids.welcome_label:
            self.ids.welcome_label.text = f"Welcome, {value}"
        else:
            print("welcome_label is None")

    def print_values(self):
        print(f"Current username: {self.user_name}")
        print(f"Current welcome label text: {self.ids.welcome_label.text}")
