"""
============================================================
VISUALISASI 3D FESTIVAL LAMPION BOROBUDUR
Simulasi Gerak Partikel Berbasis OpenGL

Mata Kuliah : Grafika Komputer
Bahasa      : Python 3
Library     : PyOpenGL, Pygame, NumPy
============================================================

INSTALASI (MacOS):
    python3 -m pip install PyOpenGL pygame numpy

CARA JALANKAN:
    python3 borobudur_festival.py

KONTROL KAMERA:
    Mouse drag kiri  → Rotasi kamera
    Scroll wheel     → Zoom in/out
    R                → Reset kamera
    SPACE            → Pause/resume animasi
    +/-              → Tambah/kurangi jumlah lampion
    Q / ESC          → Keluar
============================================================
"""

import sys
import math
import random
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from borobudur_build import draw_borobudur
from tanah import *
from lampion import *
from kamera import *
from lighting import *
from config import *
from hud import *


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def main():
    pygame.init()

    pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 24)
    pygame.display.gl_set_attribute(pygame.GL_DOUBLEBUFFER, 1)

    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H), DOUBLEBUF | OPENGL)
    pygame.display.set_caption(TITLE)

    # Font
    try:
        font_sm = pygame.font.SysFont("Courier New", 14)
        font_lg = pygame.font.SysFont("Courier New", 18, bold=True)
    except Exception:
        font_sm = pygame.font.Font(None, 18)
        font_lg = pygame.font.Font(None, 22)

    # ── OpenGL setup ──────────────────────────
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glShadeModel(GL_SMOOTH)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, WINDOW_W / WINDOW_H, 0.5, 300.0)
    glMatrixMode(GL_MODELVIEW)

    setup_lighting()

    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)

    # ── Scene objects ─────────────────────────
    camera = Camera()
    ps = ParticleSystem(MAX_PARTICLES)

    stars = []
    for _ in range(600):
        th = random.uniform(0, 2 * math.pi)
        ph = random.uniform(0.05, math.pi / 2)
        r = 85.0
        b = random.uniform(0.4, 1.0)
        stars.append(
            (
                r * math.sin(ph) * math.cos(th),
                r * math.cos(ph),
                r * math.sin(ph) * math.sin(th),
                b,
            )
        )

    # Surface HUD (reused setiap frame)
    hud_surf = pygame.Surface((WINDOW_W, WINDOW_H), pygame.SRCALPHA)

    paused = False
    mouse_down = False
    last_mx = last_my = 0
    clock = pygame.time.Clock()

    print("=" * 50)
    print("  Festival Lampion Borobudur — OpenGL")
    print("  Drag mouse → rotasi | Scroll → zoom")
    print("  SPACE → pause | +/- → jumlah lampion")
    print("=" * 50)

    running = True
    while running:
        clock.tick(FPS)
        fps = clock.get_fps()

        for ev in pygame.event.get():
            if ev.type == QUIT:
                running = False
            elif ev.type == KEYDOWN:
                if ev.key in (K_q, K_ESCAPE):
                    running = False
                elif ev.key == K_SPACE:
                    paused = not paused
                elif ev.key == K_r:
                    camera.reset()
                elif ev.key in (K_PLUS, K_EQUALS, K_KP_PLUS):
                    ps.max_p = min(500, ps.max_p + 20)
                elif ev.key in (K_MINUS, K_KP_MINUS):
                    ps.max_p = max(10, ps.max_p - 20)
            elif ev.type == MOUSEBUTTONDOWN:
                if ev.button == 1:
                    mouse_down = True
                    last_mx, last_my = ev.pos
                elif ev.button == 4:
                    camera.zoom(1)
                elif ev.button == 5:
                    camera.zoom(-1)
            elif ev.type == MOUSEBUTTONUP:
                if ev.button == 1:
                    mouse_down = False
            elif ev.type == MOUSEMOTION and mouse_down:
                camera.rotate((ev.pos[0] - last_mx) * 0.4, -(ev.pos[1] - last_my) * 0.4)
                last_mx, last_my = ev.pos

        keys = pygame.key.get_pressed()

        speed = 0.4

        if keys[K_w]:
            camera.move_relative(forward=-speed)

        if keys[K_s]:
            camera.move_relative(forward=speed)

        if keys[K_a]:
            camera.move_relative(right=-speed)

        if keys[K_d]:
            camera.move_relative(right=speed)

        if keys[K_q]:
            camera.move_relative(up=-speed)

        if keys[K_e]:
            camera.move_relative(up=speed)

        # ── Update ────────────────────────────
        if not paused:
            ps.update()

        # ── Render 3D scene ───────────────────
        glClearColor(0.02, 0.03, 0.10, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        camera.apply()

        glDisable(GL_LIGHTING)
        draw_stars(stars)
        draw_ground()

        glEnable(GL_LIGHTING)
        draw_borobudur(quadric)

        ps.render(quadric)  # lampion (sudah disable lighting di dalam)

        # ── Render HUD sebagai texture quad ───
        render_hud_texture(hud_surf, font_sm, font_lg, ps, paused, fps)
        draw_hud_quad(hud_surf)

        pygame.display.flip()

    gluDeleteQuadric(quadric)
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
