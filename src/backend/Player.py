from kivy.uix.screenmanager import Screen
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.button import Button
from database.database import connect, get_current_number
from kivy.properties import StringProperty, ObjectProperty
import os
from kivy.app import App
from kivy.uix.popup import Popup
from jnius import autoclass


class VideoPlayerApp(Screen):
    info_message = StringProperty("")



    def play_video(self, instance):
        with connect():
            number = get_current_number()
        user_data_dir = App.get_running_app().user_data_dir
        user_folder_path = os.path.join(user_data_dir, str(number))
        file_chooser = FileChooserListView(path=user_folder_path)
        popup = Popup(title="Выберите видео", content=file_chooser, size_hint=(0.8, 0.8))
        valid_name = number
        #self.vid = VideoPlayer(source='video.mp4', state='play')

        def on_file_selected(instance, selection):
            if selection:
                selected = selection[0]
            #if self.ids.filechooser.selection:
            #    selected = self.ids.filechooser.selection[0]
                filename = os.path.basename(selected)
                if filename.startswith(valid_name):
                    self.ids.video_player.source = selected
                    self.ids.video_player.state = 'play'
                    self.info_message = ''
                else:
                    self.info_message = 'Choose YOUR video'
            popup.dismiss()
        file_chooser.bind(selection=on_file_selected)
        popup.open()

        #return self.vid
    def delete_video(self):
        with connect():
            number = get_current_number()
        valid_name = number
        user_data_dir = App.get_running_app().user_data_dir
        user_folder_path = os.path.join(user_data_dir, str(number))
        file_chooser = FileChooserListView(path=user_folder_path)
        popup = Popup(title="Выберите видео", content=file_chooser, size_hint=(0.8, 0.8))
        def on_file_selected(instance, selection):
            if selection:
                selected = selection[0]
                filename = os.path.basename(selected)
                if filename.startswith(valid_name):
        #if self.ids.filechooser.selection:
            #selected = self.ids.filechooser.selection[0]
                    try:
                        os.remove(selected)
                        from kivy.clock import Clock
                        Clock.schedule_once(lambda dt: file_chooser._update_files(), -1)
                        #self.ids.filechooser._update_files()  # Обновите список файлов после удаления
                    except OSError as e:
                        #print(f"Ошибка: {e}")
                        self.info_message= 'Error'
                else:
                    self.info_message = 'Choose YOUR video'
            popup.dismiss()
        file_chooser.bind(selection=on_file_selected)
        popup.open()