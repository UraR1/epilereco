from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.app import App  # Ensure to import App
from database.database import create_user, is_username_available


class SignupScreen(BoxLayout):
    error_message = StringProperty("Create an Account")

    def signup(self, username, password, confirm_password):
        if is_username_available(username):
            if password == confirm_password:
                create_user(username, password)
                self.error_message = "Create an Account"
                App.get_running_app().root.current = 'login'
            else:
                self.error_message = "Passwords do not match!"
        else:
            self.error_message = "Username already exists"