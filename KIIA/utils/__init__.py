from importlib.metadata import version, PackageNotFoundError
from .tools.speech import speak
from utils.tools.logger import print

installed = {}
missing = []

with open("requirements.txt", "r") as f:
    packages = [
        line.strip()
        for line in f
        if line.strip() and not line.startswith("#")
    ]

for pkg in packages:
    try:
        installed[pkg] = version(pkg)
    except PackageNotFoundError:
        missing.append(pkg)

if not missing:
    speak("All packages are installed.")
    print("All packages are installed.")
else:
    speak("Some packages are missing. Please install them.")
    print("Missing packages:")
    for pkg in missing:
        print(f"  {pkg}")

print("\nInstalled packages:")
for pkg, ver in installed.items():
    print(f"  {pkg}: {ver}")
