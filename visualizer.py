# Monica Yuol Manyok — DJ Festival Visualizer v2 ✨
# Professional neon bar visualizer with color transitions & reflections

import pygame
import numpy as np
import soundfile as sf
import sounddevice as sd
import math

# === SETTINGS === #
AUDIO_FILE = "DammyDee-Uk-Drill-type-freebeat.wav"
WIDTH, HEIGHT = 1280, 720
FPS = 60
BAR_COUNT = 100
SENSITIVITY = 3.8
DECAY = 0.35
BG_COLOR = (3, 3, 10)
COLOR_SPEED = 0.8  # speed of color cycling

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎧 Monica's DJ Festival Visualizer v2")
clock = pygame.time.Clock()

# === LOAD AUDIO === #
data, samplerate = sf.read(AUDIO_FILE)
if len(data.shape) > 1:
    data = data.mean(axis=1)
sd.play(data, samplerate)

chunk = int(samplerate / FPS)
bars = np.zeros(BAR_COUNT)

def color_cycle(t):
    """Smooth RGB color cycling over time"""
    r = int(127 * math.sin(t * COLOR_SPEED) + 128)
    g = int(127 * math.sin(t * COLOR_SPEED + 2) + 128)
    b = int(127 * math.sin(t * COLOR_SPEED + 4) + 128)
    return (r, g, b)

# === MAIN LOOP === #
running = True
i = 0
t = 0
while running and i + chunk < len(data):
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sd.stop()
            pygame.quit()
            exit()

    frame = data[i:i + chunk]
    i += chunk

    yf = np.abs(np.fft.fft(frame)[:BAR_COUNT])
    yf = np.log1p(yf) * SENSITIVITY
    bars = (1 - DECAY) * bars + DECAY * yf

    # background fade
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(80)
    overlay.fill(BG_COLOR)
    screen.blit(overlay, (0, 0))

    # color change
    bar_color = color_cycle(t)
    t += 0.05

    bar_width = WIDTH / BAR_COUNT
    for k in range(BAR_COUNT):
        bar_height = int(bars[k] * 8)
        x = int(k * bar_width)
        y = HEIGHT - bar_height

        # reflection
        pygame.draw.rect(screen, (bar_color[0]//4, bar_color[1]//4, bar_color[2]//4),
                         (x, HEIGHT - bar_height//2, bar_width - 2, bar_height//2))

        # glow base
        glow = (min(255, bar_color[0]+40),
                min(255, bar_color[1]+40),
                min(255, bar_color[2]+40))
        pygame.draw.rect(screen, glow, (x-1, y-6, bar_width+2, bar_height*1.2))

        # main bar
        pygame.draw.rect(screen, bar_color, (x, y, bar_width-2, bar_height))

    # bass flash
    bass = np.mean(bars[:15])
    flash = min(150, int(bass * 3))
    if flash > 10:
        flash_color = (flash, flash//2, flash)
        screen.fill(flash_color, special_flags=pygame.BLEND_ADD)

    pygame.display.flip()
    clock.tick(FPS)

sd.stop()
pygame.quit()
