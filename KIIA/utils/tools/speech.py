import subprocess
import numpy as np
import sounddevice as sd
import os
from utils.tools.write_log import write_log

path = os.path.expandvars(r"C:\KIIA_modules\modules\piper")
PIPER_PATH = os.path.join(path, "piper.exe")
MODEL_PATH = os.path.join(path, "en_US-amy-medium.onnx")

DEFAULT_SPEED = 5.0

def lspeak(audio, speed=DEFAULT_SPEED):
    process = subprocess.Popen(
        [PIPER_PATH, "--model", MODEL_PATH, "--output-raw", "--speed", str(speed)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    )

    process.stdin.write(audio.encode("utf-8"))
    process.stdin.close()

    raw_audio = process.stdout.read()
    process.wait()

    saudio = np.frombuffer(raw_audio, dtype=np.int16)
    sd.play(saudio, 22050)
    sd.wait()

def speak(text, speed=2.0):
    write_log("KIIA", text)
    return lspeak(text, speed)
