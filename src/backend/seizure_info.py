import cv2
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from database.database import connect, is_valid_date_seconds, is_number, stop_recording, start_recording, get_current_number

class SeizureInfoScreen(Screen):
    info_message = StringProperty("")
    def get_patient_names(self):
        with connect() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT name, surname, patronymic, birth_date FROM patient")
            result = cursor.fetchall()
            patient_name = [" ".join(row) for row in result]
        return patient_name

    def save_seizure_info(self, seizure_start, seizure_duration, seizure_type):
        with connect() as connection:
            #if patient_name != "Select Patient":
                if is_valid_date_seconds(seizure_start):
                    if is_number(seizure_duration):
                        try:
                            self.info_message = "Success!"
                            cursor = connection.cursor()
                            number = get_current_number()
                            cursor.execute(
                                '''SELECT name, surname, patronymic, birth_date FROM patient WHERE number = ? ''',
                                (number,))
                            result = cursor.fetchall()
                            for row in result:
                                name, surname, patronymic, birth_date = row
                            patient_name = f"{name} {surname} {patronymic} ({birth_date})"
                            cursor.execute("INSERT INTO seizure (number, seizure_start, seizure_duration, seizure_type, patient_name) VALUES (?, ?, ?, ?, ?)", (number, seizure_start, seizure_duration, seizure_type, patient_name))
                            connection.commit()
                        except:
                            self.info_message = "No patient data"
                    else:
                        self.info_message = "Invalid Duration"
                else:
                    self.info_message = "Invalid Date"
            #else:
                #self.info_message = "Invalid Patient"

#@    def start_recording(self, instance):
#
 #           self.recording = True
 #           self.start_button.disabled = True
 #           self.stop_button.disabled = False
 #           self.capture = cv2.VideoCapture(0)
 #           self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
 #           self.out = cv2.VideoWriter('output.avi', self.fourcc, 20.0, (640, 480))
 #           Clock.schedule_once(self.update, 1 / 30.)


 #   def stop_recording(self, instance):
 #       self.recording = False
 #       self.start_button.disabled = False
 #       self.stop_button.disabled = True
 #       self.capture.release()
 #       self.out.release()
 #       cv2.destroyAllWindows()

  #  def update(self, dt):
  #      if self.recording:
  #          ret, frame = self.capture.read()
  #          if ret:
  #              # Save frame to video file
  #              self.out.write(frame)

                # Convert the frame to texture
   #             buf1 = cv2.flip(frame, 0)
   #             buf = buf1.tostring()
   #             image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
   #             image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

                # Display image from the texture
    #            self.image.texture = image_texture

     #       Clock.schedule_once(self.update, 1 / 30.)
