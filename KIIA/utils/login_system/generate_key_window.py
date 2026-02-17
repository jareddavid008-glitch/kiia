from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
from .auth_core import create_session

class GenerateKeyWindow(QWidget):
    def __init__(self, on_done=None):
        super().__init__()
        self.on_done = on_done

        self.setWindowTitle("Generate Security Key")
        self.resize(400, 150)

        self.output = QTextEdit()
        self.output.setReadOnly(True)

        btn = QPushButton("Generate 366-Day Key")
        btn.clicked.connect(self.generate)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Your security key:"))
        layout.addWidget(self.output)
        layout.addWidget(btn)

    def generate(self):
        token = create_session()
        self.output.setText(token)

        if self.on_done:
            self.on_done()
