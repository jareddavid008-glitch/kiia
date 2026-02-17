from PyQt6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QLabel
)
from .....tools.speech import speak
from .....tools.CommandWindow import CommandWindow
import tempfile
import os

class TempFileLauncherWindow(CommandWindow):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        self.setWindowTitle("Open Temporary File")
        self.resize(450, 180)

        self.run_temp_btn = QPushButton("Open Temp File")
        self.status_label = QLabel("Status: Idle")

        self.run_temp_btn.clicked.connect(self.open_temp_file)

        layout = QVBoxLayout(self)
        layout.addWidget(self.run_temp_btn)
        layout.addWidget(self.status_label)

    def open_temp_file(self):
        try:
            temp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
            temp.write(b"This is a dynamically created temporary file.\nHello from Python!")
            temp.close()

            os.startfile(temp.name)

            self.status_label.setText("Status: Temporary file opened")
            speak("Temporary file opened successfully")
            
        except Exception as e:
            self.status_label.setText("Status: Failed to open temp file")
            speak("Failed to open temporary file")
            print("Error:", e)
