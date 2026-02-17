from PyQt6.QtWidgets import (
    QWidget, 
    QLabel, 
    QPushButton, 
    QVBoxLayout, 
    QHBoxLayout,
    QMessageBox
)
from ..functions.blocked import blocked_comm, admin_conf
from .speech import speak

class AdminConfirmDialog(QWidget):
    def __init__(self, command, on_allow):
        super().__init__()
        self.on_allow = on_allow

        self.setWindowTitle("Administrator Permission")
        self.resize(360, 120)

        label = QLabel(
            f"The command '{command}' may modify system settings.\n"
            "Do you want to continue?"
        )

        btn_yes = QPushButton("Yes")
        btn_no = QPushButton("No")

        btn_yes.clicked.connect(self.allow)
        btn_no.clicked.connect(self.deny)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_yes)
        btn_layout.addWidget(btn_no)

        layout = QVBoxLayout(self)
        layout.addWidget(label)
        layout.addLayout(btn_layout)

        speak(f"Permission required for {command}")

    def allow(self):
        self.close()
        self.on_allow()

    def deny(self):
        speak("Command execution cancelled.")
        self.close()

def _extract_command(program: str) -> str:
    return program.lower().split("\\")[-1].split(".")[0]

def check_and_execute(window, program: str, arguments: list):
    base_cmd = _extract_command(program)

    if base_cmd in blocked_comm:
        speak(f"The command {base_cmd} is restricted.")
        window.controller.log(f"Blocked command: {base_cmd}")
        return

    if base_cmd in admin_conf:
        dialog = AdminConfirmDialog(base_cmd, window)

        if dialog.exec() != dialog.Accepted:
            speak("Command execution cancelled.")
            window.controller.log(f"Admin command denied: {base_cmd}")
            return

        window.start_process(program, arguments)
        speak("Command executed with administrator permission.")
        return

    window.start_process(program, arguments)
    speak("Command executed successfully.")