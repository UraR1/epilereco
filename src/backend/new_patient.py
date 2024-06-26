import cv2
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from database.database import connect, is_patient_available, is_valid_date, start_recording, stop_recording, get_current_number, get_current_user, is_number_available, is_login_valid, is_only_letters
import datetime
import time

class NewPatientScreen(Screen):
    info_message = StringProperty("")
    number_message = StringProperty("")

    def unique_code(self):
        with connect() as connection:
            current_number = get_current_number()
            self.number_message = str(current_number)
            #cursor = connection.cursor()

    def save_patient(self, name,surname, patronymic, birth_date, sex):
        with connect() as connection:
            if is_login_valid(name) and is_login_valid(surname) and is_login_valid(patronymic) and is_login_valid(birth_date) and is_login_valid(sex):
                if is_only_letters(name) and is_only_letters(surname) and is_only_letters(patronymic):
                    if is_valid_date(birth_date):
                        if sex != "Select Sex":
                            number = get_current_number()
                            if is_number_available(number):
                                self.info_message = "Success!"
                                cursor = connection.cursor()
                                cursor.execute("INSERT INTO patient (name,surname, patronymic, birth_date, sex, number, doctor) VALUES (?, ?, ?, ?, ?, ?, 1)", (name,surname,patronymic, birth_date, sex, number))
                                connection.commit()
                            else:
                                self.info_message = "Delete your data first"
                        else:
                            self.info_message = "Invalid sex!"
                    else:
                        self.info_message = "Invalid date!"
                else:
                    self.info_message = "Only letters available!"
            else:
                self.info_message = "Empty fields!"
    def delete_patient(self):
        with connect() as connection:
            number = get_current_number()
            cursor = connection.cursor()
            cursor.execute('''DELETE FROM patient WHERE number = ?''', (number,))
            connection.commit()
            self.info_message = "Done"
