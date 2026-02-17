from PyQt6.QtWidgets import (
    QPushButton,
    QVBoxLayout, QLabel
)
from .....tools.speech import speak
from .....tools.CommandWindow import CommandWindow

class ServicesWindow(CommandWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Services.msc Information")
        self.resize(350, 100)

        speak("Gathering system information.")

        self.label = QLabel("Click execute to display hostname information")

        self.btn = QPushButton("Execute")
        self.btn.clicked.connect(self.run_services)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.btn)

    def run_services(self):
        self.start_process("cmd", ["/c", "services.msc"])
        speak("Please Check the output sir.")
