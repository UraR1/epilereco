from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.app import App
from database.database import validate_login
from kivy.utils import platform

class LoginScreen(BoxLayout):
    error_message = StringProperty("")

    def login(self, username, password):
        if platform == "android":
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE,Permission.CAMERA, Permission.WRITE_EXTERNAL_STORAGE])
        if validate_login(username, password):
            self.error_message = ""
            app = App.get_running_app()
            app.root.get_screen('main').main.set_user(username)  # Modify this line
            app.root.current = 'main'
        else:
            self.error_message = "Login failed!"
