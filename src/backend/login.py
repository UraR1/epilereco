from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.app import App
import platform

from database.database import validate_login_p, validate_login_d, set_current_user, get_current_user, set_current_number, get_current_number, set_current_number_d, get_current_number_d
#from kivy.utils import platform

class LoginScreen(BoxLayout):
    error_message = StringProperty("")

    def login(self, username, password, role):
        os_name = platform.system()
        if os_name == 'Linux':
            # Запрос разрешений для Android
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.CAMERA, Permission.WRITE_EXTERNAL_STORAGE, Permission.INTERNET, Permission.READ_EXTERNAL_STORAGE])
        if role == 'Patient':
            if validate_login_p(username, password):
                set_current_user(role)
                set_current_number(username)
                if username == 'Admin':
                    set_current_user(username)
                    app = App.get_running_app()
                    app.root.get_screen('main').main.set_user(username)
                    app.root.current = 'main'
                else:
                    self.error_message = ""
                    app = App.get_running_app()
                    app.root.get_screen('patient').patient.set_user(username)
                    app.root.current = 'patient'
            else:
                self.error_message = "Login failed!"
        elif role == 'Doctor':
            if validate_login_d(username, password):
                set_current_user(role)
                set_current_number_d(username)
                self.error_message = ""
                app = App.get_running_app()
                app.root.get_screen('doctor').doctor.set_user(username)
                app.root.current = 'doctor'
            else:
                self.error_message = "Login failed!"
        else:
            self.error_message = "Choose your role!"

