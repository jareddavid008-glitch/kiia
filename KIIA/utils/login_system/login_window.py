from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import QTimer
from .auth_core import validate_token
from ..tools.speech import speak

class LoginWindow(QWidget):
    def __init__(self, on_success):
        super().__init__()
        self.on_success = on_success

        self.setWindowTitle("Secure Login")
        self.resize(400, 150)

        self.label = QLabel("Enter your security token:")
        self.input = QLineEdit()
        self.input.setPlaceholderText("Paste your token here")

        self.btn = QPushButton("Login")
        self.btn.clicked.connect(self.login)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.btn)

    def login(self):
        token = self.input.text().strip()

        if not token:
            QMessageBox.warning(self, "Error", "Token required")
            speak("Please Paste the token")
            return

        if validate_token(token):
            speak("Login successful")
            QMessageBox.information(self, "Success", "Login successful")
            self.on_success()
            QTimer.singleShot(200, self.close)
            
        else:
            QMessageBox.critical(self, "Denied", "Invalid or expired token")
            speak("Invalid or expired token")