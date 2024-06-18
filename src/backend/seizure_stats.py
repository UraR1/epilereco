from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from database.database import connect, get_current_number_d, get_current_number
from datetime import datetime, timedelta

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
                equals2.execute('''SELECT number FROM patient WHERE doctor = ? AND number = ? ''', (number_d,number_p,))
                equals_d = equals2.fetchone()[0]
                if equals_d == equals_p:
                    cursor = connection.cursor()
                    current_date = datetime.now()
                    date_10_days_ago = (current_date - timedelta(days=10)).strftime(
                        '%Y.%m.%d')  # Вычитаем 10 дней и преобразуем в строку
                    date_30_days_ago = (current_date - timedelta(days=30)).strftime(
                        '%Y.%m.%d')

                    cursor.execute('''
                                    SELECT COUNT(*) / COUNT(DISTINCT DATE(seizure_start)) 
                                    FROM seizure 
                                    WHERE patient_name = ?
                                ''', (patient_name,))
                    average_daily_seizures = cursor.fetchone()[0] or 1
                    cursor.execute('''
                                   SELECT AVG(seizure_duration) 
                                   FROM seizure 
                                   WHERE patient_name = ? AND seizure_start >= ? AND seizure_start <= ?
                               ''', (patient_name, date_10_days_ago, current_date.strftime('%Y.%m.%d')))
                    average_duration_last_10_days = cursor.fetchone()[0] or 0
                    cursor.execute('''
                                   SELECT AVG(seizure_duration) 
                                   FROM seizure 
                                   WHERE patient_name = ? AND seizure_start BETWEEN ? AND ?
                               ''', (patient_name, date_30_days_ago, current_date.strftime('%Y.%m.%d')))
                    average_duration_last_30_days = cursor.fetchone()[0] or 0
                    cursor.execute('''
                                    SELECT MAX(seizure_duration), MIN(seizure_duration) 
                                    FROM seizure 
                                    WHERE patient_name = ?
                                ''', (patient_name,))
                    longest_seizure, shortest_seizure = cursor.fetchone()
                    cursor.execute(f"SELECT AVG(seizure_duration) FROM seizure WHERE patient_name = '{patient_name}'")
                    result = cursor.fetchone()[0]
                    self.text_label = (
                        f"Статистика для пациента {patient_name}:\n"
                        f"Среднее количество приступов в день: {average_daily_seizures}\n"
                        f"Средняя продолжительность приступа за последние 10 дней: {average_duration_last_10_days}\n"
                        f"Средняя продолжительность приступа за последние 30 дней: {average_duration_last_30_days}\n"
                        f"Самый длинный приступ: {longest_seizure}\n"
                        f"Самый короткий приступ: {shortest_seizure}\n"
                        f"Средняя продолжительность приступов за все время: {result}"
                    )
                else:
                    print(number_d, number_p,equals_p, equals2, equals_d)
                    self.text_label = "Wrong Patient"
        except:
            self.text_label = "Wrong Patient or no Stats"


