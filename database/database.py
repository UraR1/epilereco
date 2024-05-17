import sqlite3
import datetime

import cv2

DB_PATH = "database/my_epilemob.db"

def connect():
    return sqlite3.connect(DB_PATH)

def setup_db():
    with connect() as connection:
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS patient (id INTEGER PRIMARY KEY, name TEXT,surname TEXT, patronymic TEXT, birth_date DATE, sex TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS seizure (id INTEGER PRIMARY KEY, patient_name TEXT, seizure_start DATE, seizure_duration INTEGER, seizure_type TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS video (patient_id INTEGER, video_name TEXT)''')
        # ... Additional table creation here
        connection.commit()

def create_user(username, password):
    with connect() as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, password))
        connection.commit()

def get_user_id_by_name(name):
    with connect() as connection:
        cursor = connection.cursor()
        cursor.execute('''SELECT id FROM patient WHERE name = ?''', (name,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

def insert_video(user_id, video_name):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Video (user_id, video_name) VALUES (?, ?)', (user_id, video_name))
    conn.commit()
    conn.close()
def validate_login(username, password):
    with connect() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
    return user is not None

def is_username_available(username: str) -> bool:
    with connect() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT username FROM user WHERE username = ?", (username,))
        return cursor.fetchone() is None

def is_patient_available(name,surname,patronymic, birth_date: str) -> bool:
    with connect() as connection:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM patient WHERE name='{name}' AND surname='{surname}' AND patronymic='{patronymic}' AND birth_date ='{birth_date}'")
        return cursor.fetchone() is None
def is_valid_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%d.%m.%Y')
        return True
    except ValueError:
        return False

def is_valid_date_seconds(date_text):
    try:
        datetime.datetime.strptime(date_text, '%d.%m.%Y %H:%M:%S')
        return True
    except ValueError:
        return False
def is_number(number):
    try:
        float(number)
        return True
    except ValueError:
        return False
def start_recording(self, instance):
    self.recording = True
    self.out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480))

    self.start_button.disabled = True
    self.stop_button.disabled = False

def stop_recording(self, instance):
    self.recording = False
    self.out.release()

    self.start_button.disabled = False
    self.stop_button.disabled = True

def update(self, dt):
    if self.recording:
        ret, frame = self.capture.read()
        self.out.write(frame)
#def is_surname_available(surname, name: str) -> bool:
#    with connect() as connection:
#        cursor = connection.cursor()
#        cursor.execute("SELECT surname FROM patient WHERE name = ?, surname = ?", (name, surname,))
#        return cursor.fetchone() is None

#def is_fathername_available(fathername: str) -> bool:
#    with connect() as connection:
#        cursor = connection.cursor()
#        cursor.execute("SELECT fathername FROM patient WHERE fathername = ?", (fathername,))
#        return cursor.fetchone() is None