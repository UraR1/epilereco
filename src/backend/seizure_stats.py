from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from database.database import connect

class SeizureStatsScreen(Screen):
    text_label = StringProperty("")
    def get_patient_names(self):
        with connect() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM patient")
            result = cursor.fetchall()
            patient_name = [row[0] for row in result]
        return patient_name
        pass

    def show_statistics(self, patient_name):
        with connect() as connection:
            self.text_label = "Statistics will be shown here."
            cursor = connection.cursor()
            cursor.execute(f"SELECT AVG(seizure_duration) FROM seizure WHERE patient_name = '{patient_name}'")
            result = cursor.fetchone()[0]
        self.text_label = (f"Среднее значение длительности приступа\n для пациента {patient_name} равно  {result}.")

