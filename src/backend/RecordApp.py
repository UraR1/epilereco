
import os
import shutil
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
import cv2
import datetime
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ObjectProperty
from database.database import connect
#from kivy.utils import platform
#from android import request_permissions, Permission

class RecordAppScreen(Screen):
    info_message = StringProperty("")
    image = Image()
    video_texture = ObjectProperty(None)
    def start_recording(self, instance,patient_id):
        self.recording = True
        self.capture = cv2.VideoCapture(0)
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        now = datetime.datetime.now()
        date_string = now.strftime("%Y-%m-%d_%H-%M-%S")  # Формат: ГГГГ-ММ-ДД_ЧЧ-ММ-СС
        filename = f"videos/output_{date_string}.avi"
        self.out = cv2.VideoWriter(filename, self.fourcc, 20.0, (640, 480))
        Clock.schedule_once(self.update, 1 / 30.)
        with connect() as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO video (patient_id,video_name) VALUES (?, ?)", (patient_id,date_string))
            connection.commit()
    def get_patient_id(self):
        with connect() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT Id FROM patient")
            result = cursor.fetchall()
            patient_id = [" ".join(map(str, row)) for row in result]
        return patient_id
   # def save_video_info(self, patient_id,video_name):
    #    with connect() as connection:
   #         cursor = connection.cursor()
    #        cursor.execute("INSERT INTO video (patient_id,video_name) VALUES (?, ?)", (patient_id,video_name))
    #        connection.commit()
    def save_comment(self, comment):
        # Получаем текущую дату и время
        now = datetime.datetime.now()
        date_string = now.strftime("%Y-%m-%d_%H-%M-%S")  # Формат: ГГГГ-ММ-ДД_ЧЧ-ММ-СС

        # Создаем имя файла с текущей датой и временем
        filename = f"videos/comments_{date_string}.txt"
        with open(filename, 'a') as file:
            file.write(comment + '\n')
        print(f'Комментарий сохранен в файл {filename}')
    def stop_recording(self, instance):
        self.recording = False
        self.capture.release()
        self.out.release()
        #self.save_comment()
        #cv2.destroyAllWindows()

    def update(self, dt):
        if self.recording:
            ret, frame = self.capture.read()
            if ret:
                # Save frame to video file
                self.out.write(frame)

                # Convert the frame to texture
                buf1 = cv2.flip(frame, 0)
                buf = buf1.tostring()
                image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

                # Display image from the texture
                self.video_texture = image_texture

            Clock.schedule_once(self.update, 1 / 30.)

    def upload_video(self, instance):

        file_chooser = FileChooserListView(path='.')
        popup = Popup(title="Выберите видео", content=file_chooser, size_hint=(0.8, 0.8))
        def on_file_selected(instance, selection):
            if selection:
                selected_file = selection[0]
                #print(f"Выбран файл: {selected_file}")
                target_folder = "upload_videos"
                try:
                    shutil.move(selected_file, target_folder)
                    #print(f"Файл успешно перемещен в {target_folder}")
                    self.info_message = f"Файл успешно перемещен в {target_folder}"
                except Exception as e:
                    #print(f"Ошибка при перемещении файла: {e}")
                    self.info_message = f"Ошибка при перемещении файла: {e}"
            popup.dismiss()
        file_chooser.bind(selection=on_file_selected)
        popup.open()
        #ошибка файл уже создан, сделать так, чтобы файл менял название в зависимости от пользователя из бд