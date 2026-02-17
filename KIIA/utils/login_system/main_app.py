from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Protected Application")

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Welcome to the secured system"))
