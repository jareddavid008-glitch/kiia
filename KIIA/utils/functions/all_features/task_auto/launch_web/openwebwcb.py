from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QLabel, QComboBox
from .....tools.speech import speak
from .....tools.CommandWindow import CommandWindow
from .....tools.logger import LoggedLineEdit
import webbrowser

BROWSERS = {
    "Chrome": "C:\Program Files\Google\Chrome\Applicationchrome.exe %s",
}

class ChosenBrowserLauncherWindow(CommandWindow):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        self.setWindowTitle("Open URL in Chosen Browser")
        self.resize(450, 220)

        self.url_input = LoggedLineEdit()
        self.browser_select = QComboBox()
        self.run_btn = QPushButton("Open URL")
        self.status_label = QLabel("Status: Idle")

        self.browser_select.addItems(BROWSERS.keys())
        self.url_input.textChanged.connect(lambda text: self.run_btn.setEnabled(bool(text.strip())))
        self.run_btn.clicked.connect(self.open_url)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("URL:"))
        layout.addWidget(self.url_input)
        layout.addWidget(QLabel("Browser:"))
        layout.addWidget(self.browser_select)
        layout.addWidget(self.run_btn)
        layout.addWidget(self.status_label)

    def open_url(self):
        url = self.url_input.text().strip()
        browser_name = self.browser_select.currentText()

        if not url:
            self.status_label.setText("Status: No URL provided")
            speak("Please provide a URL")
            return

        try:
            browser_path = BROWSERS[browser_name]
            webbrowser.register(browser_name, None, webbrowser.BackgroundBrowser(browser_path))
            webbrowser.get(browser_name).open(url, new=2)
            self.status_label.setText(f"Status: URL opened in {browser_name}")
            speak(f"URL opened in {browser_name} successfully")

        except Exception as e:
            self.status_label.setText("Status: Failed to open URL")
            speak("Failed to open URL")
            print("Error:", e)
