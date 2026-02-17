import builtins
from utils.tools.write_log import write_log
from PyQt6.QtWidgets import QLineEdit

class LoggedLineEdit(QLineEdit):
    def __init__(self, controller=None, label="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = controller
        self.label = label

    def focusOutEvent(self, event):
        text = self.text().strip()
        if text:
            write_log("USER", f"{self.label}: {text}")

            if self.controller:
                self.controller.log(f"USER_INPUT [{self.label}]: {text}")

        super().focusOutEvent(event)

# Logging print
def print(*args, **kwargs):
    message = " ".join(str(arg) for arg in args)
    write_log("KIIA", message)
    builtins.print(*args, **kwargs)

# Logging input
def input(prompt=""):
    user_value = builtins.input(prompt)
    write_log("USER", f"{prompt}{user_value}")
    return user_value