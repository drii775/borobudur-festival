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

# ─────────────────────────────────────────────
#  KONFIGURASI GLOBAL
# ─────────────────────────────────────────────
WINDOW_W, WINDOW_H = 1024, 768
TITLE = "Festival Lampion Borobudur - Visualisasi 3D"
FPS = 60

MAX_PARTICLES = 150
SPAWN_RATE = 2
PARTICLE_MIN_Y = -8.0
PARTICLE_MAX_Y = 28.0


# ─────────────────────────────────────────────
#  KELAS: PARTIKEL LAMPION
# ─────────────────────────────────────────────
class LampionParticle:
    COLOR_PALETTE = [
        (1.0, 0.85, 0.20),
        (1.0, 0.60, 0.10),
        (1.0, 0.35, 0.10),
        (1.0, 0.80, 0.40),
        (1.0, 0.95, 0.70),
        (1.0, 0.50, 0.00),
        (0.9, 0.20, 0.10),
    ]

    def __init__(self):
        self.reset()

    def reset(self):
        spread = 13.0
        self.x = random.uniform(-spread, spread)
        self.y = PARTICLE_MIN_Y + random.uniform(-2, 2)
        self.z = random.uniform(-spread, spread)

        self.vy = random.uniform(0.04, 0.10)
        self.vx = random.uniform(-0.008, 0.008)
        self.vz = random.uniform(-0.008, 0.008)

        self.osc_amp = random.uniform(0.002, 0.007)
        self.osc_speed = random.uniform(1.0, 3.0)
        self.osc_phase = random.uniform(0, 2 * math.pi)

        self.color = random.choice(self.COLOR_PALETTE)
        self.size = random.uniform(0.20, 0.50)

        self.age = 0
        self.life = random.uniform(180, 380)
        self.alpha = 0.0

    def update(self, time):
        self.age += 1
        self.y += self.vy
        self.x += (
            self.vx + math.sin(time * self.osc_speed + self.osc_phase) * self.osc_amp
        )
        self.z += self.vz

        fade = 30
        if self.age < fade:
            self.alpha = self.age / fade
        elif self.age > self.life - fade:
            self.alpha = (self.life - self.age) / fade
        else:
            self.alpha = 1.0
        self.alpha = max(0.0, min(1.0, self.alpha))

        return self.y > PARTICLE_MAX_Y or self.age >= self.life


# ─────────────────────────────────────────────
#  KELAS: SISTEM PARTIKEL
# ─────────────────────────────────────────────
class ParticleSystem:
    def __init__(self, max_p=MAX_PARTICLES):
        self.max_p = max_p
        self.particles = []
        self.time = 0.0

    def update(self):
        self.time += 0.016
        self.particles = [p for p in self.particles if not p.update(self.time)]
        need = min(SPAWN_RATE, self.max_p - len(self.particles))
        for _ in range(need):
            self.particles.append(LampionParticle())

    def render(self, q):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDisable(GL_LIGHTING)

        for p in self.particles:
            r, g, b = p.color
            s = p.size

            glPushMatrix()
            glTranslatef(p.x, p.y, p.z)
            glScalef(s, s * 1.5, s)

            # Badan lampion (silinder)
            glColor4f(r, g, b, p.alpha * 0.90)
            gluCylinder(q, 0.40, 0.40, 0.80, 10, 3)

            # Tutup atas
            glPushMatrix()
            glTranslatef(0, 0, 0.80)
            glColor4f(r * 0.85, g * 0.85, b * 0.85, p.alpha * 0.90)
            gluDisk(q, 0, 0.40, 10, 1)
            glPopMatrix()

            # Tutup bawah
            glColor4f(r * 0.80, g * 0.80, b * 0.80, p.alpha * 0.90)
            gluDisk(q, 0, 0.40, 10, 1)

            # Efek glow
            glColor4f(r, g, b * 0.5, p.alpha * 0.25)
            gluSphere(q, 0.60, 8, 6)

            glPopMatrix()

        glDisable(GL_BLEND)


# # ─────────────────────────────────────────────
# #  GAMBAR CANDI BOROBUDUR
# # ─────────────────────────────────────────────


# ─────────────────────────────────────────────
#  TANAH & BINTANG
# ─────────────────────────────────────────────
def draw_ground():
    glDisable(GL_LIGHTING)
    glColor3f(0.08, 0.14, 0.06)
    glBegin(GL_QUADS)
    glVertex3f(-80, -0.02, -80)
    glVertex3f(80, -0.02, -80)
    glVertex3f(80, -0.02, 80)
    glVertex3f(-80, -0.02, 80)
    glEnd()


def draw_stars(stars):
    glDisable(GL_LIGHTING)
    glPointSize(1.8)
    glBegin(GL_POINTS)
    for x, y, z, b in stars:
        glColor3f(b, b, min(1.0, b * 1.1))
        glVertex3f(x, y, z)
    glEnd()
    glPointSize(1.0)


# ─────────────────────────────────────────────
#  PENCAHAYAAN
# ─────────────────────────────────────────────
def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.30, 0.30, 0.35, 1.0])

    glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 18.0, 0.0, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.65, 0.65, 0.70, 1.0])
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.02)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.001)

    glLightfv(GL_LIGHT1, GL_POSITION, [-20.0, 30.0, -10.0, 1.0])
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.30, 0.35, 0.50, 1.0])


# ─────────────────────────────────────────────
#  KAMERA
# ─────────────────────────────────────────────
class Camera:
    def __init__(self):
        self.reset()

    def reset(self):
        self.dist = 38.0
        self.yaw = 30.0
        self.pitch = 22.0
        self.tx, self.ty, self.tz = 0.0, 5.0, 0.0

    def apply(self):
        glLoadIdentity()
        yr = math.radians(self.yaw)
        pr = math.radians(self.pitch)
        ex = self.tx + self.dist * math.cos(pr) * math.sin(yr)
        ey = self.ty + self.dist * math.sin(pr)
        ez = self.tz + self.dist * math.cos(pr) * math.cos(yr)
        gluLookAt(ex, ey, ez, self.tx, self.ty, self.tz, 0, 1, 0)

    def rotate(self, dy, dp):
        self.yaw += dy
        self.pitch = max(-80, min(80, self.pitch + dp))

    def zoom(self, d):
        self.dist = max(6, min(90, self.dist - d * 2.5))

    def move(self, dx, dy, dz):
        self.tx += dx
        self.ty += dy
        self.tz += dz

    def move_relative(self, forward=0, right=0, up=0):

        yr = math.radians(self.yaw)

        fx = math.sin(yr)
        fz = math.cos(yr)

        rx = math.cos(yr)
        rz = -math.sin(yr)

        self.tx += fx * forward + rx * right
        self.tz += fz * forward + rz * right
        self.ty += up


# ─────────────────────────────────────────────
#  HUD — render teks sebagai texture quad
#  (glDrawPixels tidak didukung di MacOS modern)
# ─────────────────────────────────────────────
def render_hud_texture(hud_surf, font_sm, font_lg, ps, paused, fps):
    hud_surf.fill((0, 0, 0, 0))

    # Judul
    s = font_lg.render("Festival Lampion Borobudur", True, (255, 215, 80))
    hud_surf.blit(s, (14, 10))

    # Info panel
    lines = [
        f"Lampion aktif : {len(ps.particles)}",
        f"Maks lampion  : {ps.max_p}",
        f"FPS           : {fps:.0f}",
        f"Status        : {'PAUSED' if paused else 'RUNNING'}",
    ]
    for i, ln in enumerate(lines):
        hud_surf.blit(font_sm.render(ln, True, (200, 200, 180)), (14, 48 + i * 22))

    # Kontrol (pojok kiri bawah)
    ctrl = [
        "[ KONTROL ]",
        "Drag    → Rotasi kamera",
        "Scroll  → Zoom",
        "SPACE   → Pause / lanjut",
        "+  /  - → Jumlah lampion",
        "R       → Reset kamera",
        "ESC / Q → Keluar",
    ]
    y0 = WINDOW_H - len(ctrl) * 21 - 12
    for i, ln in enumerate(ctrl):
        col = (255, 215, 80) if i == 0 else (150, 150, 130)
        hud_surf.blit(font_sm.render(ln, True, col), (14, y0 + i * 21))


def draw_hud_quad(hud_surf):
    """Upload hud_surf sebagai OpenGL texture, gambar sebagai fullscreen quad."""
    tex_data = pygame.image.tostring(hud_surf, "RGBA", True)

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGBA,
        WINDOW_W,
        WINDOW_H,
        0,
        GL_RGBA,
        GL_UNSIGNED_BYTE,
        tex_data,
    )

    # Switch ke proyeksi ortho 2D
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, WINDOW_W, 0, WINDOW_H, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(1, 1, 1, 1)

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(0, 0)
    glTexCoord2f(1, 0)
    glVertex2f(WINDOW_W, 0)
    glTexCoord2f(1, 1)
    glVertex2f(WINDOW_W, WINDOW_H)
    glTexCoord2f(0, 1)
    glVertex2f(0, WINDOW_H)
    glEnd()

    glDisable(GL_TEXTURE_2D)
    glDisable(GL_BLEND)
    glEnable(GL_DEPTH_TEST)

    # Restore matrices
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

    glDeleteTextures([tex_id])


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
