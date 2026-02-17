from PyQt6.QtWidgets import (
    QPushButton,
    QVBoxLayout, QLabel
)
from .....tools.speech import speak
from .....tools.CommandWindow import CommandWindow

class DevmgmtWindow(CommandWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Device Manager GUI")
        self.resize(350, 100)

        speak("Gathering system information.")

        self.label = QLabel("Click execute to display system information")

        self.btn = QPushButton("Execute")
        self.btn.clicked.connect(self.run_devmgmt)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.btn)

    def run_devmgmt(self):
        self.start_process("cmd", ["/c", "devmgmt.msc"])
        speak("Please Check the output sir.")


class DxdiagWindow(CommandWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Device Manager GUI")
        self.resize(350, 100)

        speak("Gathering system information.")

        self.label = QLabel("Click execute to display system information")

        self.btn = QPushButton("Execute")
        self.btn.clicked.connect(self.run_dxdiag)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.btn)

    def run_dxdiag(self):
        self.start_process("cmd", ["/c", "dxdiag"])
        speak("Please Check the output sir.")

class Msinfo32Window(CommandWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Device Manager GUI")
        self.resize(350, 100)

        speak("Gathering system information.")

        self.label = QLabel("Click execute to display system information")

        self.btn = QPushButton("Execute")
        self.btn.clicked.connect(self.run_msinfo32)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.btn)

    def run_msinfo32(self):
        self.start_process("cmd", ["/c", "msinfo32"])
        speak("Please Check the output sir.")

