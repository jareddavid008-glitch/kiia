from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QLabel, QSpinBox
from .....tools.speech import speak
from .....tools.CommandWindow import CommandWindow
import webbrowser
import subprocess
import time

class LocalhostLauncherWindow(CommandWindow):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        self.setWindowTitle("Open Local Web App")
        self.resize(450, 200)

        self.port_input = QSpinBox()
        self.port_input.setMinimum(1)
        self.port_input.setMaximum(65535)
        self.port_input.setValue(8000)

        self.run_btn = QPushButton("Open Localhost Web App")
        self.status_label = QLabel("Status: Idle")

        self.run_btn.clicked.connect(self.open_localhost)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Localhost Port:"))
        layout.addWidget(self.port_input)
        layout.addWidget(self.run_btn)
        layout.addWidget(self.status_label)

    def open_localhost(self):
        port = self.port_input.value()
        url = f"http://localhost:{port}"

        try:
            webbrowser.open(url, new=2)
            self.status_label.setText(f"Status: Opened {url}")
            speak(f"Local web app opened at port {port}")
        except Exception as e:
            self.status_label.setText("Status: Failed to open web app")
            speak("Failed to open local web app")
            print("Error:", e)
