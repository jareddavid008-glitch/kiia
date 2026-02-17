import subprocess
import sys
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

EXECUTION_MODES = {
    "Fire-and-Forget (Background)": "background",
    "Parent-Child Linked": "linked",
    "Detach from Parent": "detached"
}

class BackgroundExecutionWindow(CommandWindow):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        self.setWindowTitle("Background vs Foreground Execution")
        self.resize(470, 260)

        self.exe_input = LoggedLineEdit()
        self.mode_select = QComboBox()
        self.args_input = LoggedLineEdit()
        self.run_btn = QPushButton("Run")

        self.mode_select.addItems(EXECUTION_MODES.keys())
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
        layout.addWidget(QLabel("Execution Mode"))
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

    def run_exe(self):
        exe = self.exe_input.text().strip()
        args = self.args_input.text().split() if self.args_input.text() else []
        mode = EXECUTION_MODES[self.mode_select.currentText()]

        try:
            if mode == "background":
                # Fire-and-forget: parent does not wait
                subprocess.Popen(
                    [exe] + args,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                speak("Application started in background")

            elif mode == "linked":
                subprocess.Popen([exe] + args)
                speak("Application started linked to parent")

            elif mode == "detached":
                if sys.platform == "win32":
                    subprocess.Popen(
                        [exe] + args,
                        creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
                        close_fds=True
                    )
                else:
                    subprocess.Popen(
                        [exe] + args,
                        start_new_session=True,
                        close_fds=True
                    )

                speak("Application detached from parent process")

        except Exception as e:
            speak("Failed to launch application")
            print(f"Error: {e}")

        QTimer.singleShot(200, self.close)
