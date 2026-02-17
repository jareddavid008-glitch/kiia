import subprocess
import win32con
from .speech import speak

WINDOW_MODES = {
    "Normal": win32con.SW_SHOWNORMAL,
    "Hidden": win32con.SW_HIDE,
    "Minimized": win32con.SW_SHOWMINIMIZED,
    "Maximized": win32con.SW_SHOWMAXIMIZED,
}

def launch_process(exe_path, args=None, window_mode="normal"):
    speak("How would you like to open the page sir.")
    speak("Please Select the op")
    if args is None:
        args = []

    startup = subprocess.STARTUPINFO()
    startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow = WINDOW_MODES.get(
        window_mode.lower(),
        win32con.SW_SHOWNORMAL
    )

    return subprocess.Popen(
        [exe_path, *args],
        startupinfo=startup
    )
