from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.app import App
from database.database import validate_login

class LoginScreen(BoxLayout):
    error_message = StringProperty("")

    def login(self, username, password):
        if validate_login(username, password):
            self.error_message = ""
            app = App.get_running_app()
            app.root.get_screen('main').main.set_user(username)  # Modify this line
            app.root.current = 'main'
        else:
            self.error_message = "Login failed!"
