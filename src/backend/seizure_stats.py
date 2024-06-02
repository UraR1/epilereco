from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from database.database import connect, get_current_number_d, get_current_number

class SeizureStatsScreen(Screen):
    text_label = StringProperty("")
    def get_patient_names(self):
        patient_names = []
        with connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                '''SELECT name, surname, patronymic, birth_date FROM patient''')
            result = cursor.fetchall()
            for row in result:
                name, surname, patronymic, birth_date = row
                full_name = f"{name} {surname} {patronymic} ({birth_date})"
                patient_names.append(full_name)

            #patient_name = [" ".join(row) for row in result]
        return patient_names

    def show_statistics(self, patient_name):
        try:
            with connect() as connection:
                number_d = get_current_number_d()
                cursor_p = connection.cursor()
                cursor_p.execute(f"SELECT number FROM seizure WHERE patient_name = '{patient_name}'")
                number_p = str(cursor_p.fetchone()[0])
                equals = connection.cursor()
                equals.execute('''SELECT number FROM patient WHERE number = ? ''', (number_p,))
                equals_p = equals.fetchone()[0]
                equals2 = connection.cursor()
                equals2.execute('''SELECT number FROM patient WHERE doctor = ? ''', (number_d,))
                equals_d = equals2.fetchone()[0]
                if equals_d == equals_p:
                    cursor = connection.cursor()
                    cursor.execute(f"SELECT AVG(seizure_duration) FROM seizure WHERE patient_name = '{patient_name}'")
                    result = cursor.fetchone()[0]
                    self.text_label = (f"Среднее значение длительности приступа\n для пациента {patient_name} равно  {result}.")
                else:
                    self.text_label = "Wrong Patient"
        except:
            self.text_label = "Wrong Patient or no Stats"


