from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
import random
from kivy.app import App  # Ensure to import App
from database.database import create_user_p,create_user_d, is_username_available_p, is_username_available_d


class SignupScreen(BoxLayout):
    error_message = StringProperty("Create an Account")

    def signup(self, username, password, confirm_password, role):
        if role == 'Patient':
            if is_username_available_p(username):
                if password == confirm_password:
                    number = random.randint(1000000000, 9999999999)
                    create_user_p(username, password, role, number)
                    self.error_message = "Welcome!"
                    App.get_running_app().root.current = 'login'
                else:
                    self.error_message = "Passwords do not match!"
            else:
                self.error_message = "Patient already exists"
        else:

            if is_username_available_d(username):
                if password == confirm_password:
                    number = random.randint(1000000000, 9999999999)
                    create_user_d(username, password, role, number)
                    self.error_message = "Welcome!"
                    App.get_running_app().root.current = 'login'
                else:
                    self.error_message = "Passwords do not match!"
            else:
                self.error_message = "Doctor already exists"