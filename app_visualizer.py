# Monica Yuol Manyok — Visualizer App 🎧
# Lets you pick any song and run your glowing DJ visualizer.

import tkinter as tk
from tkinter import filedialog
import threading
import pygame
import numpy as np
import soundfile as sf
import sounddevice as sd
import math

# === VISUALIZER FUNCTION === #
def run_visualizer(audio_file):
    WIDTH, HEIGHT = 1280, 720
    FPS = 60
    BAR_COUNT = 100
    SENSITIVITY = 3.8
    DECAY = 0.35
    BG_COLOR = (3, 3, 10)
    COLOR_SPEED = 0.8

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("🎧 Monica's DJ Visualizer App")
    clock = pygame.time.Clock()

    data, samplerate = sf.read(audio_file)
    if len(data.shape) > 1:
        data = data.mean(axis=1)
    sd.play(data, samplerate)

    chunk = int(samplerate / FPS)
    bars = np.zeros(BAR_COUNT)

    def color_cycle(t):
        r = int(127 * math.sin(t * COLOR_SPEED) + 128)
        g = int(127 * math.sin(t * COLOR_SPEED + 2) + 128)
        b = int(127 * math.sin(t * COLOR_SPEED + 4) + 128)
        return (r, g, b)

    i, t = 0, 0
    running = True
    while running and i + chunk < len(data):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sd.stop()
                pygame.quit()
                return

        frame = data[i:i + chunk]
        i += chunk
        yf = np.abs(np.fft.fft(frame)[:BAR_COUNT])
        yf = np.log1p(yf) * SENSITIVITY
        bars = (1 - DECAY) * bars + DECAY * yf

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(80)
        overlay.fill(BG_COLOR)
        screen.blit(overlay, (0, 0))

        bar_color = color_cycle(t)
        t += 0.05
        bar_width = WIDTH / BAR_COUNT

        for k in range(BAR_COUNT):
            bar_height = int(bars[k] * 8)
            x = int(k * bar_width)
            y = HEIGHT - bar_height

            # Reflection
            pygame.draw.rect(screen, (bar_color[0]//4, bar_color[1]//4, bar_color[2]//4),
                            (x, HEIGHT - bar_height//2, bar_width - 2, bar_height//2))

            # Glow + Main Bar
            glow = (min(255, bar_color[0]+40),
                    min(255, bar_color[1]+40),
                    min(255, bar_color[2]+40))
            pygame.draw.rect(screen, glow, (x-1, y-6, bar_width+2, bar_height*1.2))
            pygame.draw.rect(screen, bar_color, (x, y, bar_width-2, bar_height))

        bass = np.mean(bars[:15])
        flash = min(150, int(bass * 3))
        if flash > 10:
            flash_color = (flash, flash//2, flash)
            screen.fill(flash_color, special_flags=pygame.BLEND_ADD)

        pygame.display.flip()
        clock.tick(FPS)

    sd.stop()
    pygame.quit()

# === APP WINDOW === #
def choose_file():
    file_path = filedialog.askopenfilename(
        title="Choose a song",
        filetypes=[("Audio Files", "*.wav *.mp3")])
    if file_path:
        threading.Thread(target=run_visualizer, args=(file_path,), daemon=True).start()

root = tk.Tk()
root.title("🎶 Monica's Audio Visualizer App")
root.geometry("400x250")
root.config(bg="#0a0a1a")

label = tk.Label(root, text="🎧 Choose your song to visualize 🎧", bg="#0a0a1a", fg="white", font=("Segoe UI", 14))
label.pack(pady=40)

btn = tk.Button(root, text="🎵 Choose Song", font=("Segoe UI", 14), bg="#1e90ff", fg="white", command=choose_file)
btn.pack(pady=20)

quit_btn = tk.Button(root, text="❌ Quit", font=("Segoe UI", 12), bg="#444", fg="white", command=root.destroy)
quit_btn.pack(pady=10)

root.mainloop()
