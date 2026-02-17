import pyaudio
import numpy as np
import time
import math
import sys
from .CommandWindow import CommandWindow
from ..tools.speech import speak
from utils.tools.logger import print
from PyQt6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QApplication
)

def wait_for_sound(threshold=150, timeout=10):
    CHUNK = 1024
    RATE = 44100

    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    print("Waiting for sound...")
    start_time = time.time()

    try:
        while True:
            if time.time() - start_time > timeout:
                return False

            data = stream.read(CHUNK, exception_on_overflow=False)
            samples = np.frombuffer(data, dtype=np.int16).astype(np.float32)

            if samples.size == 0:
                continue

            rms = np.sqrt(np.mean(samples ** 2))
            if math.isnan(rms):
                continue

            if rms > threshold:
                print("Sound detected:", int(rms))
                return True

    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

class controller:
    def __init__(self):
        self.ask_window = None

    def start(self):
        self.ask_window = AskWindow(self)
        self.ask_window.show()

    def on_mic_ok(self):
        print("Mic OK")

    def on_mic_failed(self):
        print("Mic failed")

    def on_skip_mic(self):
        print("Mic check skipped")

class AskWindow(CommandWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Asking Confirmation")
        self.resize(350, 100)

        self.label = QLabel("Want to check mic?")

        self.btn_yes = QPushButton("Yes")
        self.btn_no = QPushButton("No")

        self.btn_yes.clicked.connect(self.on_yes)
        self.btn_no.clicked.connect(self.on_no)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_yes)
        btn_layout.addWidget(self.btn_no)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addLayout(btn_layout)

    def on_yes(self): 
        speak("Please make a sound to continue.") 

        detected = wait_for_sound() 
        
        if detected: 
            speak("Sound detected") 
            speak("ALright we'll be moving forward without any issues.") 
        else: 
            speak("No sound detected. CHeck the mic.") 
            
    def on_no(self): 
        speak("No worries we'll be continuing")
        self.close()

def askmic():
    app = QApplication(sys.argv)

    speak("Mind sir, before we start I am checking the mic.")

    ctrl = controller()
    ctrl.start()

    app.exec()
