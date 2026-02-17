from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer, QProcess
import locale

class CommandWindow(QWidget):
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