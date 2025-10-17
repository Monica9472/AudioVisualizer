# final_make_exe.py
# Author: Monica Yuol Manyok
import os, sys, subprocess, shutil

def main():
    print("🧹 Cleaning old builds...")
    for f in ["build", "dist", "app_visualizer.spec"]:
        if os.path.exists(f):
            if os.path.isdir(f): shutil.rmtree(f)
            else: os.remove(f)

    print("📦 Installing all required modules...")
    subprocess.run([sys.executable, "-m", "pip", "install",
                    "pyinstaller", "sounddevice", "numpy", "pygame", "matplotlib", "--upgrade"])

    print("🏗 Building executable...")
    subprocess.run([
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--noconsole",
        "--add-data", "C:\\Users\\monic\\Downloads\\audio-visualizer\\.venv\\Lib\\site-packages\\sounddevice;.",
        "--hidden-import", "sounddevice",
        "--hidden-import", "_sounddevice_data",
        "--hidden-import", "numpy",
        "--hidden-import", "pygame",
        "--hidden-import", "matplotlib",
        "app_visualizer.py"
    ])

    print("\n✅ Build complete! Check the 'dist' folder for your .exe file.")

if __name__ == "__main__":
    main()
