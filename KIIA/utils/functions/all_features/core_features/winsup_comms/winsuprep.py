from PyQt6.QtWidgets import (
    QPushButton,
    QVBoxLayout, QLabel
)
from .....tools.speech import speak
from .....tools.CommandWindow import CommandWindow


class ScannowWindow(CommandWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Resource Monitor GUI.")
        self.resize(350, 100)

        speak("Gathering system information.")

        self.label = QLabel("Click execute to display system information")

        self.btn = QPushButton("Execute")
        self.btn.clicked.connect(self.run_scannow)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.btn)

    def run_scannow(self):
        self.start_process("cmd", ["/c", "sfc", "/scannow"])
        speak("Please Check the output sir.")

class RestorehealthWindow(CommandWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Resource Monitor GUI.")
        self.resize(350, 100)

        speak("Gathering system information.")

        self.label = QLabel("Click execute to display system information")

        self.btn = QPushButton("Execute")
        self.btn.clicked.connect(self.run_restorehealth)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.btn)

    def run_restorehealth(self):
        self.start_process("cmd", ["/c", "dism", "/online", "/cleanup-image", "/restorehealth"])
        speak("Please Check the output sir.")

class WuaucltWindow(CommandWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Resource Monitor GUI.")
        self.resize(350, 100)

        speak("Gathering system information.")

        self.label = QLabel("Click execute to display system information")

        self.btn = QPushButton("Execute")
        self.btn.clicked.connect(self.run_wuauclt)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.btn)

    def run_wuauclt(self):
        self.start_process("cmd", ["/c", "wuauclt"])
        speak("Please Check the output sir.")
