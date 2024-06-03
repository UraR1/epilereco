from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.app import App
import platform

from database.database import validate_login_p, validate_login_d, set_current_user, get_current_user, set_current_number, get_current_number, set_current_number_d, get_current_number_d
#from kivy.utils import platform

class LoginScreen(BoxLayout):
    error_message = StringProperty("")

    def login(self, username, password, role):
        #print(platform)
        if role == 'Patient':
            if validate_login_p(username, password):
                set_current_user(role)
                set_current_number(username)
                if username == 'Admin':
                    set_current_user(username)
                    app = App.get_running_app()
                    app.root.get_screen('main').main.set_user(username)  # Modify this line
                    app.root.current = 'main'
                    #current_user = get_current_user()
                    #print(current_user)
                else:
                    self.error_message = ""
                    current_user = get_current_user()
                    #print(current_user)
                    #set_current_number(username)
                    current_number = get_current_number()
                    #print(current_number)
                    app = App.get_running_app()
                    app.root.get_screen('patient').patient.set_user(username)  # Modify this line
                    app.root.current = 'patient'
            else:
                self.error_message = "Login failed!"
        elif role == 'Doctor':
            if validate_login_d(username, password):
                set_current_user(role)
                set_current_number_d(username)
                #current_number = get_current_number_d()
                #print(current_number)
                self.error_message = ""
                app = App.get_running_app()
                app.root.get_screen('doctor').doctor.set_user(username)  # Modify this line
                app.root.current = 'doctor'
            else:
                self.error_message = "Login failed!"
        else:
            self.error_message = "Choose your role!"

