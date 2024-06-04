
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
from database.database import connect, get_current_number
from kivy.app import App
import platform
#from kivy.utils import platform
#from android import request_permissions, Permission

class RecordAppScreen(Screen):
    info_message = StringProperty("")
    image = Image()
    video_texture = ObjectProperty(None)
    recording = False

    def start_recording(self, instance):
        self.recording = True
        with connect():
            number = get_current_number()
        os_name = platform.system()
        self.info_message = os_name
        if os_name == 'Linux':
            # Запрос разрешений для Android
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.CAMERA, Permission.WRITE_EXTERNAL_STORAGE, Permission.INTERNET, Permission.READ_EXTERNAL_STORAGE])
            cap = cv2.VideoCapture(0)

            # Определяем кодек и создаем объект VideoWriter
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

            while (cap.isOpened()):
                # Захватываем кадр за кадром
                ret, frame = cap.read()
                if ret == True:
                    # Записываем кадр в файл
                    out.write(frame)

                    # Отображаем кадр
                    cv2.imshow('frame', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    break

            # Освобождаем все ресурсы
            cap.release()
            out.release()
            cv2.destroyAllWindows()
        else:
            self.capture = cv2.VideoCapture(0)
            self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
            now = datetime.datetime.now()
            date_string = now.strftime("%Y-%m-%d_%H-%M-%S")  # Формат: ГГГГ-ММ-ДД_ЧЧ-ММ-СС
            user_data_dir = App.get_running_app().user_data_dir
            # Создаем путь к папке с номером пользователя
            user_folder_path = os.path.join(user_data_dir, str(number))
            if not os.path.exists(user_folder_path):
                os.makedirs(user_folder_path)
            filename = os.path.join(user_folder_path, f"{number}_{date_string}.avi")
            # print(f'Папка "{filename}" успешно создана!')
            self.out = cv2.VideoWriter(filename, self.fourcc, 20.0, (640, 480))
            Clock.schedule_once(self.update, 1 / 30.)

            with connect() as connection:
                cursor = connection.cursor()
                number = get_current_number()
                cursor.execute("INSERT INTO video (number,video_name) VALUES (?, ?)", (number, date_string))
                connection.commit()




    def stop_recording(self, instance):
        self.recording = False
        if self.capture:
            self.capture.release()
        if self.out:
            self.out.release()
        Clock.unschedule(self.update)
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
            number = get_current_number()
            if selection:
                selected_file = selection[0]
                #print(f"Выбран файл: {selected_file}")

                user_data_dir = App.get_running_app().user_data_dir
                # Создаем путь к папке с номером пользователя
                user_folder_path = os.path.join(user_data_dir, str(number))
                now = datetime.datetime.now()
                date_string = now.strftime("%Y-%m-%d_%H-%M-%S")  # Формат: ГГГГ-ММ-ДД_ЧЧ-ММ-СС
                filename = os.path.join(user_folder_path, f"{number}_{date_string}.avi")
                target_folder = "upload_videos"
                try:
                    shutil.move(selected_file, filename)
                    #print(f"Файл успешно перемещен в {target_folder}")
                    self.info_message = f"Файл успешно перемещен в {filename}"
                except Exception as e:
                    #print(f"Ошибка при перемещении файла: {e}")
                    self.info_message = f"Ошибка при перемещении файла: {e}"
            popup.dismiss()
        file_chooser.bind(selection=on_file_selected)
        popup.open()
        #ошибка файл уже создан, сделать так, чтобы файл менял название в зависимости от пользователя из бд
    def save_comment(self, comment):
        # Получаем текущую дату и время
        now = datetime.datetime.now()
        number = get_current_number()
        date_string = now.strftime("%Y-%m-%d_%H-%M-%S")  # Формат: ГГГГ-ММ-ДД_ЧЧ-ММ-СС

        # Создаем имя файла с текущей датой и временем
        user_data_dir = App.get_running_app().user_data_dir
        # Создаем путь к папке с номером пользователя
        user_folder_path = os.path.join(user_data_dir, str(number))
        if not os.path.exists(user_folder_path):
            os.makedirs(user_folder_path)
        filename = os.path.join(user_folder_path, f"{number}_{date_string}.txt")
        with open(filename, 'a') as file:
            file.write(comment + '\n')
        #print(f'Комментарий сохранен в файл {filename}')