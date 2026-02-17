import sys
from PyQt6.QtWidgets import QApplication
from utils.login_system.security import start_security
from utils.functions.ui import ControlPanel
from utils.tools.speech import speak
from utils.tools.logger import print
from utils.tools.mic_check import askmic
from datetime import datetime
import speech_recognition as sr

def WishMe():
    hour = datetime.now().hour
    if hour < 12:
        speak("Good Morning Sir!")
    elif hour < 18:
        speak("Good Afternoon Sir!")
    else:
        speak("Good Evening Sir!")
    speak("What Can I Do For You")

def takeCommand():
    try:
        r = sr.Recognizer()
       
        with sr.Microphone() as source:
            print("Listening....")
            r.energy_threshold = 400
            audio = r.listen(source)
        try:
            print("Recognizing...")
            command = r.recognize_google(audio, language='en-in').lower()
            print(f'You said: {command}')
        except:
            print('Please try again')
            command = takeCommand()
        return command
    except Exception as e:
        print(e)
        return  False
        
def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    def launch_main_ui():
        win = ControlPanel()
        win.show()
        WishMe()

    start_security(on_success=launch_main_ui)

    sys.exit(app.exec())

if __name__ == "__main__":
    askmic()
    main()
