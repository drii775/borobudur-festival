import math
import random

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

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
