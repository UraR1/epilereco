import sqlite3
import datetime

import cv2

DB_PATH = "database/my_epilemob.db"

def connect():
    return sqlite3.connect(DB_PATH)

def setup_db():
    with connect() as connection:
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS patient (id INTEGER PRIMARY KEY, name TEXT,surname TEXT, patronymic TEXT, birth_date DATE, sex TEXT, number TEXT, doctor TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS user_p (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT, number TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS user_d (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT, number TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS seizure (id INTEGER PRIMARY KEY, number INTEGER, patient_name TEXT, seizure_start DATE, seizure_duration INTEGER, seizure_type TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS video (number TEXT, video_name TEXT)''')
        #cursor.execute('''CREATE TABLE IF NOT EXISTS doctor_list (id INTEGER PRIMARY KEY, number TEXT, number_p TEXT)''')
        #cursor.execute('''DROP TABLE patient''')
        #cursor.execute('''DROP TABLE user_p''')
        #cursor.execute('''DROP TABLE user_d''')
        #cursor.execute('''DROP TABLE seizure''')
        #cursor.execute('''DROP TABLE video''')
        #cursor.execute('''DROP TABLE doctor_list''')
        #cursor.execute('''DROP TABLE doctor''')
        # ... Additional table creation here
        connection.commit()
def set_current_user(role):
    global current_user
    current_user = role
def get_current_user():
    return current_user
def set_current_number(username):
    with connect() as connection:
        cursor = connection.cursor()
        cursor.execute('''SELECT number FROM user_p WHERE username = ?''', (username,))
        number = cursor.fetchone()
        global current_number
        current_number = str(number[0])
def set_current_number_d(username):
    with connect() as connection:
        cursor = connection.cursor()
        cursor.execute('''SELECT number FROM user_d WHERE username = ?''', (username,))
        number = cursor.fetchone()
        global current_number_d
        current_number_d = str(number[0])

def get_current_number():
    return current_number
def get_current_number_d():
    return current_number_d
def create_user_p(username, password, role, number):
    with connect() as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO user_p (username, password, role, number) VALUES (?, ?, ?, ?)", (username, password, role, number))
        connection.commit()
def create_user_d(username, password, role, number):
    with connect() as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO user_d (username, password, role, number) VALUES (?, ?, ?, ?)", (username, password, role, number))
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
def is_patient(number):
    with connect() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT number FROM user_p WHERE number = ?", (number,))
        return cursor.fetchone() is None
def is_number_available(number):
    with connect() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT number FROM patient WHERE number = ?", (number,))
        return cursor.fetchone() is None
def validate_login_p(username, password):
    with connect() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_p WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
    return user is not None
def validate_login_d(username, password):
    with connect() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_d WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
    return user is not None

def is_username_available_p(username: str) -> bool:
    with connect() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT username FROM user_p WHERE username = ?", (username,))
        return cursor.fetchone() is None
def is_username_available_d(username: str) -> bool:
    with connect() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT username FROM user_d WHERE username = ?", (username,))
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
        datetime.datetime.strptime(date_text, '%d.%m.%Y')
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