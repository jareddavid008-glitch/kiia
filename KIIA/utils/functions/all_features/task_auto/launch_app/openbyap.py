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
from .....tools.win_launcher import launch_process

WINDOW_MODES = {
    "Normal": "normal",
    "Minimized": "minimized",
    "Maximized": "maximized",
    "Hidden": "hidden"
}

class OpenExeWindow(CommandWindow):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        self.setWindowTitle("Executable Launcher")
        self.resize(420, 230)

        self.exe_input = LoggedLineEdit()
        self.mode_select = QComboBox()
        self.args_input = LoggedLineEdit()
        self.run_btn = QPushButton("Run")

        self.mode_select.addItems(WINDOW_MODES.keys())
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
        layout.addWidget(QLabel("Window mode"))
        layout.addWidget(self.mode_select)
        layout.addWidget(QLabel("Arguments"))
        layout.addWidget(self.args_input)
        layout.addWidget(self.run_btn)

    def on_path_changed(self, text):
        valid = bool(text.strip())
        self.mode_select.setEnabled(valid)
        self.run_btn.setEnabled(valid)

    def on_mode_changed(self, mode):
        self.args_input.setVisible(mode == "Normal")

    def run_exe(self):
        exe = self.exe_input.text().strip()
        mode = WINDOW_MODES[self.mode_select.currentText()]
        args = self.args_input.text().split() if self.args_input.isVisible() else []

        launch_process(exe, args=args, window_mode=mode)
        speak("Application started")

        QTimer.singleShot(200, self.close)