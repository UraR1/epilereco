
import os
import shutil
from kivy.uix.filechooser import FileChooserListView, FileChooserIconView
from kivy.uix.popup import Popup
import cv2
import datetime
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ObjectProperty
from database.database import connect, get_current_number
from kivy.app import App
import platform
from kivy.uix.floatlayout import FloatLayout


class RecordAppScreen(Screen):
    info_message = StringProperty("")
    video_texture = ObjectProperty(None)
    recording = False
    loadfile = ObjectProperty(None)


    def start_recording(self, instance):
        try:
            self.recording = True
            with connect():
                number = get_current_number()
            os_name = platform.system()
        #self.info_message = os_name
            if os_name == 'Linux':
                try:
                    cap = cv2.VideoCapture(0)
            # Определяем кодек и создаем объект VideoWriter
                    fourcc = cv2.VideoWriter_fourcc(*'XVID')
                    out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640, 480))
                    if cap.isOpened():
                        self.info_message = "cam opened"
                    else:
                        self.info_message = "cam closed"
                    while (cap.isOpened()):
                        ret, frame = cap.read()
                        if ret == True:
                            out.write(frame)
                            cv2.imshow('frame', frame) #check imshow
                            if cv2.waitKey(1) & 0xFF == ord('q'):
                                break
                        else:
                            break
            # Освобождаем все ресурсы
                    cap.release()
                    out.release()
                except Exception as e:
                    self.info_message = f"{e}"
            else:
                self.capture = cv2.VideoCapture(0)
                self.fourcc = cv2.VideoWriter_fourcc(*'XVID') # H264 XVID
                now = datetime.datetime.now()
                date_string = now.strftime("%Y-%m-%d_%H-%M-%S")
                user_data_dir = App.get_running_app().user_data_dir
            # Создаем путь к папке с номером пользователя
                user_folder_path = os.path.join(user_data_dir, str(number))
                if not os.path.exists(user_folder_path):
                    os.makedirs(user_folder_path)
                filename = os.path.join(user_folder_path, f"{number}_{date_string}.avi") #try MP4V
                self.out = cv2.VideoWriter(filename, self.fourcc, 20.0, (640, 480))
                Clock.schedule_once(self.update, 1 / 30.)
                with connect() as connection:
                    cursor = connection.cursor()
                    number = get_current_number()
                    cursor.execute("INSERT INTO video (number,video_name) VALUES (?, ?)", (number, date_string))
                    connection.commit()
        except:
            self.info_message = "wrong start"
    def stop_recording(self, instance):
        try:
            self.recording = False
            if self.capture:
                self.capture.release()
            if self.out:
                self.out.release()
            Clock.unschedule(self.update)
            self.info_message = "Video stopped"
        except:
            self.info_message = "Run video first"

    def update(self, dt):
        try:
            if self.recording:
                ret, frame = self.capture.read()
                if ret:
                    self.out.write(frame)
                    buf1 = cv2.flip(frame, 0)
                    buf = buf1.tostring()
                    image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                    image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                    self.video_texture = image_texture
                Clock.schedule_once(self.update, 1 / 30.)
        except:
            self.info_message = "wrong update"
    def upload_video(self, instance):
        os_name = platform.system()
        # self.info_message = os_name
        if os_name == 'Linux':
            from plyer import filechooser
            with connect():
                number = get_current_number()
            user_data_dir = App.get_running_app().user_data_dir
            user_folder_path = os.path.join(user_data_dir, str(number))
            file_chooser = FileChooserListView(path=user_folder_path, filters=(('*.avi'), ('*.mp4')))
            #path = filechooser.open_file(title="Выберите видео",size_hint=(0.8, 0.8))#, filters=[('*.avi','*.mp4')])[0] #
            #file_chooser = FileChooserListView(path=path)
        else:
            with connect():
                number = get_current_number()
            user_data_dir = App.get_running_app().user_data_dir
            user_folder_path = os.path.join(user_data_dir, str(number))
            file_chooser = FileChooserListView(path=user_folder_path , filters=(('*.avi'),('*.mp4')))
        popup = Popup(title="Выберите видео", content=file_chooser, size_hint=(0.8, 0.8), )
        def on_file_selected(instance, selection):
            number = get_current_number()
            os_name = platform.system()
            if selection:
                selected_file = selection[0]
                if os_name == 'Linux':
                    user_data_dir = '.'
                    user_folder_path = os.path.join(user_data_dir, str(number))
                    now = datetime.datetime.now()
                    date_string = now.strftime("%Y-%m-%d_%H-%M-%S")
                    filename = os.path.join(user_folder_path, f"{number}_{date_string}.avi")
                else:
                    user_data_dir = App.get_running_app().user_data_dir
                    user_folder_path = os.path.join(user_data_dir, str(number))
                    now = datetime.datetime.now()
                    date_string = now.strftime("%Y-%m-%d_%H-%M-%S")
                    filename = os.path.join(user_folder_path, f"{number}_{date_string}.avi")
                try:
                    shutil.move(selected_file, filename)
                    self.info_message = f"Файл успешно перемещен \n {filename}"
                except Exception as e:
                    self.info_message = f"{e}"
            popup.dismiss()
        file_chooser.bind(selection=on_file_selected)
        popup.open()
    def save_comment(self, comment):
        now = datetime.datetime.now()
        number = get_current_number()
        date_string = now.strftime("%Y-%m-%d_%H-%M-%S")
        user_data_dir = App.get_running_app().user_data_dir
        user_folder_path = os.path.join(user_data_dir, str(number))
        if not os.path.exists(user_folder_path):
            os.makedirs(user_folder_path)
        filename = os.path.join(user_folder_path, f"{number}_{date_string}.txt")
        with open(filename, 'a') as file:
            file.write(comment + '\n')
