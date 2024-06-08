from kivy.uix.screenmanager import Screen
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.button import Button
from database.database import connect, get_current_number
from kivy.properties import StringProperty, ObjectProperty
import os
from kivy.app import App
from kivy.uix.popup import Popup
import platform
from kivy.clock import mainthread
#from jnius import autoclass
import cv2


class VideoPlayerApp(Screen):
    info_message = StringProperty("")



    def play_video(self, instance):
        try:
            os_name = platform.system()
        # self.info_message = os_name
            if os_name == 'Linux':
                with connect():
                    number = get_current_number()
                #from plyer import filechooser
                #filechooser.open_file(title="Выберите видео", on_selection=self.handle_selected_file)
                user_data_dir = App.get_running_app().user_data_dir
                user_folder_path = os.path.join(user_data_dir, str(number))
                file_chooser = FileChooserListView(path=user_folder_path, filters=(('*.avi'), ('*.mp4')))
                popup = Popup(title="Выберите видео", content=file_chooser, size_hint=(0.8, 0.8))

                def on_file_selected(instance, selection):
                    if selection:
                        selected = selection[0]
                        filename = os.path.basename(selected)
                        self.ids.video_player.source = selected
                        self.ids.video_player.state = 'play'
                        self.info_message = 'good'

                        popup.dismiss()
                    file_chooser.bind(selection=on_file_selected)
                    popup.open()

            else:
                self.setup_file_chooser_for_other_os()
        except Exception as e:
            self.info_message = f"{e}"

    @mainthread
    def handle_selected_file(self, selection):
        if selection:
            path = selection[0]
            self.setup_file_chooser(path)
        else:
            self.info_message = 'Файл не выбран'

    def setup_file_chooser(self, path):
        try:
            file_chooser = FileChooserListView(path=path, filters=(('*.avi'), ('*.mp4')))
            self.popup = Popup(title="Выберите видео", content=file_chooser, size_hint=(0.8, 0.8))
            self.popup.open()
            file_chooser.bind(selection=self.on_file_selected)
        except:
            self.info_message = "Wrong setup file"


    def on_file_selected(self,instance, selection):
        try:
            if selection:
                selected = selection[0]
                with connect():
                    number = get_current_number()
                valid_name = number
                filename = os.path.basename(selected)
                os_name = platform.system()
                if os_name == 'Windows':
                    if filename.startswith(valid_name):
                        self.ids.video_player.source = selected
                        self.ids.video_player.state = 'play'
                        self.info_message = ''
                    else:
                        self.info_message = 'Choose YOUR video'
                else:
                    self.ids.video_player.source = selected
                    self.ids.video_player.state = 'play'
                    self.info_message = ''
            self.popup.dismiss()
            self.popup.open()
        except:
            self.info_message = "On file selected"
    def setup_file_chooser_for_other_os(self):
        with connect():
            number = get_current_number()
        user_data_dir = App.get_running_app().user_data_dir
        user_folder_path = os.path.join(user_data_dir, str(number))
        self.setup_file_chooser(user_folder_path)
    def delete_video(self):
        with connect():
            number = get_current_number()
        valid_name = number
        user_data_dir = App.get_running_app().user_data_dir
        user_folder_path = os.path.join(user_data_dir, str(number))
        file_chooser = FileChooserListView(path=user_folder_path, filters=(('*.avi'), ('*.mp4')))
        popup = Popup(title="Выберите видео", content=file_chooser, size_hint=(0.8, 0.8))
        def on_file_selected(instance, selection):
            if selection:
                selected = selection[0]
                filename = os.path.basename(selected)
                if filename.startswith(valid_name):
                    try:
                        os.remove(selected)
                        from kivy.clock import Clock
                        Clock.schedule_once(lambda dt: file_chooser._update_files(), -1)
                    except OSError as e:
                        self.info_message= 'Error'
                else:
                    self.info_message = 'Choose YOUR video'
            popup.dismiss()
        file_chooser.bind(selection=on_file_selected)
        popup.open()