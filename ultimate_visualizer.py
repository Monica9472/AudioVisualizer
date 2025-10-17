import pygame
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import sounddevice as sd
import threading
import time

# ========== CONFIG ==========
WIDTH, HEIGHT = 1000, 700
FPS = 30
AMPLITUDE = 0.5
SPEED = 0.08
COLOR = (1.0, 0.84, 0.0)  # gold
AUDIO_FILE = "SoundHelix-Song-1.wav.mp3"

# ========== WAVE SETUP ==========
x = np.linspace(-4, 4, 200)
y = np.linspace(-4, 4, 200)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

# ========== AUDIO SETUP ==========
import soundfile as sf
data, samplerate = sf.read(AUDIO_FILE, dtype='float32')
if len(data.shape) > 1:
    data = np.mean(data, axis=1)
data = data / np.max(np.abs(data))

# ========== START AUDIO ==========
def play_audio():
    sd.play(data, samplerate)
    sd.wait()

t = threading.Thread(target=play_audio)
t.start()

# ========== PLOT SETUP ==========
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')
ax.set_axis_off()
fig.patch.set_facecolor('black')

# ========== ANIMATION LOOP ==========
start_time = time.time()
while plt.fignum_exists(fig.number):
    elapsed = time.time() - start_time
    idx = int((elapsed * samplerate) % len(data))
    amp = data[idx] * AMPLITUDE
    Z = np.sin(np.sqrt(X**2 + Y**2) - elapsed * SPEED) * (amp + 0.5)
    
    ax.clear()
    ax.plot_surface(
        X, Y, Z,
        rstride=3, cstride=3,
        facecolors=cm.plasma((Z - Z.min()) / (Z.max() - Z.min())),
        linewidth=0, antialiased=True, shade=True
    )
    ax.set_zlim(-2, 2)
    ax.view_init(30, elapsed * 25)  # rotation
    ax.set_axis_off()
    plt.pause(0.03)
