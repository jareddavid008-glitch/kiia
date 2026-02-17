from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton
)

class StartWindow(QWidget):
    def __init__(self, on_have_key, on_generate_key):
        super().__init__()

        self.setWindowTitle("Security Check")
        self.resize(400, 150)

        label = QLabel("Do you already have a security key?")
        label.setStyleSheet("font-size: 16px;")

        btn_yes = QPushButton("Yes, I have a key")
        btn_no = QPushButton("No, generate a key")

        btn_yes.clicked.connect(on_have_key)
        btn_no.clicked.connect(on_generate_key)

        layout = QVBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(btn_yes)
        layout.addWidget(btn_no)
