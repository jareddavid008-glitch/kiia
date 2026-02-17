import subprocess
import ctypes
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

PERMISSION_MODES = {
    "Run as Current User": "normal",
    "Require Admin": "admin",
    "Detect Admin Only": "detect"
}

class PermissionControlWindow(CommandWindow):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        self.setWindowTitle("Permission & Context Control")
        self.resize(480, 260)

        self.exe_input = LoggedLineEdit()
        self.mode_select = QComboBox()
        self.args_input = LoggedLineEdit()
        self.run_btn = QPushButton("Run")

        self.mode_select.addItems(PERMISSION_MODES.keys())
        self.mode_select.setEnabled(False)

        self.args_input.setPlaceholderText("Optional arguments")
        self.args_input.setVisible(False)

        self.run_btn.setEnabled(False)

        self.exe_input.textChanged.connect(self.on_path_changed)
        self.mode_select.currentTextChanged.connect(self.on_mode_changed)
        self.run_btn.clicked.connect(self.run_exe)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Executable path"))
        layout.addWidget(self.exe_input)
        layout.addWidget(QLabel("Permission Mode"))
        layout.addWidget(self.mode_select)
        layout.addWidget(QLabel("Arguments"))
        layout.addWidget(self.args_input)
        layout.addWidget(self.run_btn)

    def on_path_changed(self, text):
        valid = bool(text.strip())
        self.mode_select.setEnabled(valid)
        self.run_btn.setEnabled(valid)

    def on_mode_changed(self, mode):
        self.args_input.setVisible(True)

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def run_exe(self):
        exe = self.exe_input.text().strip()
        args = self.args_input.text().split() if self.args_input.text() else []
        mode = PERMISSION_MODES[self.mode_select.currentText()]

        try:
            if mode == "normal":
                result = subprocess.run([exe] + args)
                speak("Application executed")
                print("Exit Code:", result.returncode)

            elif mode == "admin":
                if not self.is_admin():
                    speak("Requesting administrator privileges")

                    ctypes.windll.shell32.ShellExecuteW(
                        None,
                        "runas",
                        exe,
                        " ".join(args),
                        None,
                        1
                    )
                else:
                    subprocess.Popen([exe] + args)
                    speak("Already running as administrator")

            elif mode == "detect":
                if self.is_admin():
                    speak("Application running with admin privileges")
                else:
                    speak("Application not running as administrator")

        except PermissionError:
            speak("Permission denied")
            print("PermissionError occurred")

        except Exception as e:
            speak("Failed due to permission or context issue")
            print("Error:", e)

        QTimer.singleShot(200, self.close)
