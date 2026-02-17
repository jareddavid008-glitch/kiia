from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QLabel, QFileDialog
from .....tools.speech import speak
from .....tools.CommandWindow import CommandWindow
import os

class AdminLauncherWindow(CommandWindow):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        self.setWindowTitle("Run as Administrator")
        self.resize(450, 200)

        self.run_btn = QPushButton("Select File and Run as Admin")
        self.status_label = QLabel("Status: Idle")

        self.run_btn.clicked.connect(self.run_as_admin)

        layout = QVBoxLayout(self)
        layout.addWidget(self.run_btn)
        layout.addWidget(self.status_label)

    def run_as_admin(self):
        exe_path, _ = QFileDialog.getOpenFileName(self, "Select executable")
        if not exe_path:
            self.status_label.setText("Status: No file selected")
            speak("No file selected")
            return

        try:
            os.startfile(exe_path, "runas")
            self.status_label.setText("Status: Launched as admin")
            speak("Application launched as administrator")
        except Exception as e:
            self.status_label.setText("Status: Failed to launch as admin")
            speak("Failed to launch application as administrator")
            print("Error:", e)
