from datetime import datetime
import threading
import os
import json

_log_lock = threading.Lock()
_log_line_count = 0

path = os.path.expandvars("C:/Users/%USERNAME%/OneDrive/Desktop/KIIA/KIIA_OUTPUT")
path_log = os.path.join(path, "KIIA_LOG.json")

LOG_FILE = path_log

def write_log(sender, message):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "sender": sender,
        "message": message
    }

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([entry], f, indent=2)
        return

    with open(LOG_FILE, "r+") as f:
        try:
            logs = json.load(f)
        except json.JSONDecodeError:
            logs = []

        logs.append(entry)
        f.seek(0)
        json.dump(logs, f, indent=2)
        f.truncate()
