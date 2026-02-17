from PyQt6.QtWidgets import (
    QWidget, QPushButton,
    QVBoxLayout, QLabel
)
from PyQt6.QtCore import QTimer, QProcess
from .....tools.speech import speak 
from tools.logger import LoggedLineEdit
import locale

class ComWindow(QWidget):
    def start_process(self, program, arguments):
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.read_output)
        self.process.readyReadStandardError.connect(self.read_error)
        self.process.finished.connect(self.process_finished)
        self.process.start(program, arguments)

    def read_output(self):
        encoding = locale.getpreferredencoding(False)
        output = bytes(self.process.readAllStandardOutput()).decode(
            encoding, errors="replace"
        )
        self.controller.log(output)

    def read_error(self):
        encoding = locale.getpreferredencoding(False)
        error = bytes(self.process.readAllStandardError()).decode(
            encoding, errors="replace"
        )
        self.controller.log(error)

    def process_finished(self):
        QTimer.singleShot(200, self.close)

class VolWindow(ComWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Volume Information")
        self.resize(400, 100)

        speak("Please enter the directory path.")

        self.label = QLabel("Enter directory path")
        self.input = LoggedLineEdit()
        self.input.setPlaceholderText("Leave empty for current directory")

        self.btn = QPushButton("Execute")
        self.btn.clicked.connect(self.run_vol)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.btn)

    def run_vol(self):
        path = self.input.text().strip() or "."
        self.start_process("cmd", ["/c", "vol", path])
        speak("Please Check the output sir.")

class ChkdskWindow(ComWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Check Disk Integirty")
        self.resize(400, 100)

        speak("Please enter the directory path.")

        self.label = QLabel("Enter directory path")
        self.input = LoggedLineEdit()
        self.input.setPlaceholderText("Leave empty for current directory")

        self.btn = QPushButton("Execute")
        self.btn.clicked.connect(self.run_chkdsk)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.btn)

    def run_chkdsk(self):
        path = self.input.text().strip() or "."
        self.start_process("cmd", ["/c", "chkdsk", path])
        speak("Please Check the output sir.")
