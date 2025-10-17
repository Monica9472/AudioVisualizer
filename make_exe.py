import os
import subprocess
import sys

# Get current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Paths
target = os.path.join(current_dir, "app_visualizer.py")
icon_path = os.path.join(current_dir, "icon.ico")

# Install pyinstaller if missing
subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])

# Build the .exe with custom icon
subprocess.run([
    sys.executable, "-m", "PyInstaller",
    "--onefile", "--noconsole",
    "--icon", icon_path,  # ✅ Use your new icon here
    target
])

print("\n✅ Build complete! Check the 'dist' folder for your EXE with the custom icon 🎧")
