# Import all libraries needed.
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
import drive
import hashlib
import motion_detection


# Create window manager class which inherits screen manager from the kivy library.
class WindowManager(ScreenManager):
    pass


# Create the PIN PAD class which inherits screen.
class PINPad(Screen):
    # Saves the label text from the kv file as display.
    display = ObjectProperty(None)

    def save_new_pin(self, message):
        self.message_display.text = message
        # Create + Overwrite a file called "config.txt" that will store the hashed password.
        config_file = open("config.txt", "w+")
        config_file.write(self.hashed_display)
        config_file.close()

    # This method takes the user input via the parameter and uses string mantipulation to add the next digit to the end
    # if the text on the display label is not 4.
    def enter_character(self, number_clicked):
        if len(self.pin_display.text) != 4:
            self.pin_display.text = self.pin_display.text + str(number_clicked)

    # This method takes the last digit of the text on the display label and removes it.
    def backspace(self):
        if len(self.pin_display.text) != 0:
            self.pin_display.text = self.pin_display.text[0:len(self.pin_display.text) - 1]

    # This method will save the pin if it is 4 digits long.
    def enter(self):
        # print(SettingsScreen.pin_usage)
        # Checks whether the transition is from the settings screen.
        if len(self.pin_display.text) == 4:
            # Hash the pin and save it using hexadecimal.
            self.hashed_display = hashlib.sha224(self.pin_display.text.encode('utf-8')).hexdigest()
            if SettingsScreen.pin_usage == "assign":
                # Runs function to save new PIN.
                self.save_new_pin("PIN SAVED")
            if SettingsScreen.pin_usage == "verify":
                # Open the file in read mode.
                # If PIN doesn`t exist, it creates one.
                try:
                    config_file = open("config.txt", "r")
                    config_file.close()
                    # Check that the PIN is the same as the one saved in the text file.
                    # Displays error message if it is correct.
                    config_file = open("config.txt", "r")
                    if config_file.read() == self.hashed_display:
                        # Launch OpenCV window.
                        motion_detection.main()
                        # Transition to the next usage of this class.
                        SettingsScreen.pin_usage = "deactivate"
                        self.message_display.text = "Please Enter Your PIN To Deactivate the Alarm"
                    else:
                        self.message_display.text = "PIN INCORRECT"
                except:
                    self.save_new_pin("NO FILE DETECTED SO PIN ENTERED HAS BEEN SAVED. ENTER AGAIN TO LAUNCH.")
        # Error message.
        else:
            self.message_display.text = "PIN must be 4 digits!"
        # Clears text.
        self.pin_display.text = ""

    # Chooses what screen to go back to based up what screen it has come from.
    def back(self):
        if SettingsScreen.pin_usage == "assign":
            self.parent.current = "SettingsScreen"
        elif SettingsScreen.pin_usage == "verify":
            self.parent.current = "WelcomeScreen"
        self.message_display.text = ""
        self.pin_display.text = ""

    # Creates the settings screen class which inherits screen from the kivy library.


class SettingsScreen(Screen):
    # Assign variable that will be changed and can be accessed by any class.
    pin_usage = None

    def divert_to_drive_login(self):
        drive_details = drive.login()

    # This method is used to tell the PIN Pad what to do when it is transitioned to.
    def selection(self):
        # Assigns the value to all instances of this class.
        SettingsScreen.pin_usage = "assign"


# Create the first window called Welcome Screen which inherits screen from the kivy library,
class WelcomeScreen(Screen):
    def selection(self):
        # Used to identify that the PIN needs to be verified when it transitions screen.
        SettingsScreen.pin_usage = "verify"


# This variable tells the framework where the external file is which i will use for the gui layout.
formatting = Builder.load_file("stylesheet.kv")


# This is the main class that runs first and returns the style sheet.
class MotionDetectorApp(App):
    def build(self):
        return formatting


# Default kivy code needed to run the app.
if __name__ == "__main__":
    MotionDetectorApp().run()
