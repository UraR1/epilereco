from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.properties import StringProperty
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database.database import connect, get_current_number_d, get_current_user, is_number_available, is_patient

class AddNewPatientScreen(BoxLayout):

    info_message = StringProperty("")

    def get_patient_list(self):
        with connect() as connection:
            number = get_current_number_d()
            cursor = connection.cursor()
            cursor.execute('''SELECT number, name, surname, patronymic, birth_date FROM patient WHERE doctor = ? ''', (number,))
            result = cursor.fetchall()
            patient_list = [" ".join(row) for row in result]
            #print(patient_list)
        return patient_list



    def show_list(self, instance):
        popup_content = BoxLayout(orientation='vertical')
        for item in self.get_patient_list():
            label = Label(text=item)
            popup_content.add_widget(label)

        popup = Popup(title='Список', content=popup_content, size_hint=(0.8, 0.8))
        popup.open()
    #def save_patient(self,number_p):
    #    with connect() as connection:
    #        cursor = connection.cursor()
    #        number = get_current_number()
    #        cursor.execute("INSERT INTO doctor_list (number_p, number) VALUES (?, ?)", (number_p, number))
    #        connection.commit()
    def update_patient(self, number_p):
        with connect() as connection:
            if is_patient(number_p):
                self.info_message = "No such patient"
            else:
                cursor = connection.cursor()
                number = get_current_number_d()
                cursor.execute('''UPDATE patient SET doctor = ? WHERE number = ?''', (number, number_p,))
                connection.commit()
