from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from src.backend.login import LoginScreen
from src.backend.seizure_info import SeizureInfoScreen
from src.backend.seizure_stats import SeizureStatsScreen
from src.backend.RecordApp import RecordAppScreen
from src.backend.signup import SignupScreen
from src.backend.main import MainScreen
from src.backend.new_patient import NewPatientScreen
from src.backend.welcome import WelcomeScreen
from database.database import setup_db
from kivy.lang import Builder
from kivy.properties import ObjectProperty

# Load KV files
Builder.load_file('src/frontend/login.kv')
Builder.load_file('src/frontend/signup.kv')
Builder.load_file('src/frontend/main.kv')
Builder.load_file('src/frontend/welcome.kv')
Builder.load_file('src/frontend/new_patient.kv')
Builder.load_file('src/frontend/seizure_info.kv')
Builder.load_file('src/frontend/seizure_stats.kv')
Builder.load_file('src/frontend/RecordApp.kv')


class LoginScreenWrapper(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(LoginScreen())


class SignupScreenWrapper(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(SignupScreen())


class MainWrapper(Screen):
    main = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main = MainScreen()
        self.add_widget(self.main)


class WelcomeScreenWrapper(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(WelcomeScreen())


# Additional Screens
class NewPatientScreenWrapper(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(NewPatientScreen())


class SeizureInfoScreenWrapper(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(SeizureInfoScreen())


class SeizureStatsScreenWrapper(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(SeizureStatsScreen())


class RecordAppScreenWrapper(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(RecordAppScreen())


class MainApp(App):
    def build(self):
        setup_db()
        sm = ScreenManager()
        sm.add_widget(WelcomeScreenWrapper(name='welcome'))
        sm.add_widget(LoginScreenWrapper(name='login'))
        sm.add_widget(SignupScreenWrapper(name='signup'))
        sm.add_widget(MainWrapper(name='main'))
        sm.add_widget(NewPatientScreen(name='new_patient'))
        sm.add_widget(SeizureInfoScreen(name='seizure_info'))
        sm.add_widget(SeizureStatsScreen(name='seizure_stats'))
        sm.add_widget(RecordAppScreen(name='RecordApp'))
        return sm


if __name__ == '__main__':
    MainApp().run()
