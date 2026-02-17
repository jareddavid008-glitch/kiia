from .start_window import StartWindow
from .login_window import LoginWindow
from .generate_key_window import GenerateKeyWindow
from .auth_core import init_db, cleanup_expired, pre_check
from ..tools.speech import speak
from utils.tools.speech import _get_piper

_get_piper()
_windows = []

def start_security(on_success):

    init_db()
    cleanup_expired()

    if pre_check():
        speak("Login Successful")
        on_success()
        return

    def show_main():
        on_success()

    def open_login():
        login = LoginWindow(show_main)
        _windows.append(login)
        login.show()

    def open_generate():
        gen = GenerateKeyWindow(on_done=None)
        _windows.append(gen)
        gen.show()

    start = StartWindow(
        on_have_key=open_login,
        on_generate_key=open_generate
    )

    _windows.append(start)
    start.show()
