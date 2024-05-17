import cv2
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from database.database import connect, is_patient_available, is_valid_date, start_recording, stop_recording
import datetime

class NewPatientScreen(Screen):
    info_message = StringProperty("")
    def save_patient(self, name,surname, patronymic, birth_date, sex):
        with connect() as connection:
            if is_patient_available(name, surname, patronymic, birth_date):
                if is_valid_date(birth_date):
                    if sex != "Select Sex":
                        self.info_message = "Success!"
                        cursor = connection.cursor()
                        cursor.execute("INSERT INTO patient (name,surname, patronymic, birth_date, sex) VALUES (?, ?, ?, ?, ?)", (name,surname,patronymic, birth_date, sex))
                        connection.commit()
                    else:
                        self.info_message = "Invalid sex!"
                else:
                    self.info_message = "Invalid date!"
            else:
                self.info_message = "Such user exists!"

