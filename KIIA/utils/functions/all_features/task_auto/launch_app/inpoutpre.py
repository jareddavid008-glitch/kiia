import subprocess
import os
from PyQt6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QLabel,
    QComboBox
)
from PyQt6.QtCore import QTimer
from .....tools.speech import speak
from .....tools.logger import LoggedLineEdit
from .....tools.CommandWindow import CommandWindow

IO_MODES = {
    "Capture stdout": "stdout",
    "Capture stderr": "stderr",
    "Suppress Console Output": "suppress",
    "Log Output To File": "logfile"
}

class IORedirectionWindow(CommandWindow):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        self.setWindowTitle("Input / Output Redirection")
        self.resize(500, 300)

        self.exe_input = LoggedLineEdit()
        self.mode_select = QComboBox()
        self.args_input = LoggedLineEdit()
        self.logfile_input = LoggedLineEdit()
        self.run_btn = QPushButton("Run")

        self.mode_select.addItems(IO_MODES.keys())
        self.mode_select.setEnabled(False)

        self.args_input.setPlaceholderText("Optional arguments")
        self.logfile_input.setPlaceholderText("Log file path (required for Log mode)")

        self.args_input.setVisible(False)
        self.logfile_input.setVisible(False)

        self.run_btn.setEnabled(False)

        self.exe_input.textChanged.connect(self.on_path_changed)
        self.mode_select.currentTextChanged.connect(self.on_mode_changed)
        self.run_btn.clicked.connect(self.run_exe)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Executable path"))
        layout.addWidget(self.exe_input)
        layout.addWidget(QLabel("I/O Mode"))
        layout.addWidget(self.mode_select)
        layout.addWidget(QLabel("Arguments"))
        layout.addWidget(self.args_input)
        layout.addWidget(QLabel("Log File Path"))
        layout.addWidget(self.logfile_input)
        layout.addWidget(self.run_btn)

    def on_path_changed(self, text):
        valid = bool(text.strip())
        self.mode_select.setEnabled(valid)
        self.run_btn.setEnabled(valid)

    def on_mode_changed(self, mode):
        selected = IO_MODES[mode]

        self.args_input.setVisible(True)
        self.logfile_input.setVisible(selected == "logfile")

    def run_exe(self):
        exe = self.exe_input.text().strip()
        args = self.args_input.text().split() if self.args_input.text() else []
        mode = IO_MODES[self.mode_select.currentText()]

        try:
            if mode == "stdout":
                process = subprocess.Popen(
                    [exe] + args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL
                )
                output = process.communicate()[0]
                speak("Standard output captured")
                print("STDOUT:\n", output.decode(errors="ignore"))

            elif mode == "stderr":
                process = subprocess.Popen(
                    [exe] + args,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.PIPE
                )
                error = process.communicate()[1]
                speak("Standard error captured")
                print("STDERR:\n", error.decode(errors="ignore"))

            elif mode == "suppress":
                subprocess.Popen(
                    [exe] + args,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                speak("Console output suppressed")

            elif mode == "logfile":
                logfile = self.logfile_input.text().strip()

                if not logfile:
                    speak("Log file path required")
                    return

                with open(logfile, "w", encoding="utf-8") as f:
                    process = subprocess.Popen(
                        [exe] + args,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    stdout, stderr = process.communicate()

                    f.write("STDOUT:\n")
                    f.write(stdout.decode(errors="ignore"))
                    f.write("\n\nSTDERR:\n")
                    f.write(stderr.decode(errors="ignore"))

                speak("Output logged to file")

        except Exception as e:
            speak("I O redirection failed")
            print("Error:", e)

        QTimer.singleShot(200, self.close)
