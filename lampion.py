from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math

MAX_PARTICLES = 150
SPAWN_RATE = 2
PARTICLE_MIN_Y = -8.0
PARTICLE_MAX_Y = 28.0


# ─────────────────────────────────────────────
#  KELAS: PARTIKEL LAMPION
# ─────────────────────────────────────────────
class LampionParticle:

    COLOR_PALETTE = [
        (1.0, 0.75, 0.20),
        (1.0, 0.55, 0.10),
        (1.0, 0.40, 0.08),
        (1.0, 0.85, 0.40),
        (1.0, 0.95, 0.70),
    ]

    def __init__(self):
        self.reset()

    def reset(self):

        spread = 13.0

        self.x = random.uniform(-spread, spread)
        self.y = PARTICLE_MIN_Y + random.uniform(-2, 2)
        self.z = random.uniform(-spread, spread)

        self.vy = random.uniform(0.04, 0.08)
        self.vx = random.uniform(-0.004, 0.004)
        self.vz = random.uniform(-0.004, 0.004)

        self.osc_amp = random.uniform(0.002, 0.006)
        self.osc_speed = random.uniform(1.0, 2.5)
        self.osc_phase = random.uniform(0, 2 * math.pi)

        self.color = random.choice(self.COLOR_PALETTE)

        # ukuran lampion
        self.size = random.uniform(0.45, 0.75)

        self.age = 0
        self.life = random.uniform(220, 420)

        self.alpha = 0.0

    def update(self, time):

        self.age += 1

        self.y += self.vy

        self.x += (
            self.vx +
            math.sin(
                time * self.osc_speed + self.osc_phase
            ) * self.osc_amp
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

        return (
            self.y > PARTICLE_MAX_Y
            or self.age >= self.life
        )


# ─────────────────────────────────────────────
#  SISTEM PARTIKEL
# ─────────────────────────────────────────────
class ParticleSystem:

    def __init__(self, max_p=MAX_PARTICLES):

        self.max_p = max_p
        self.particles = []
        self.time = 0.0

    def update(self):

        self.time += 0.016

        self.particles = [
            p for p in self.particles
            if not p.update(self.time)
        ]

        need = min(
            SPAWN_RATE,
            self.max_p - len(self.particles)
        )

        for _ in range(need):
            self.particles.append(
                LampionParticle()
            )

    def render(self, q):

        glEnable(GL_BLEND)
        glBlendFunc(
            GL_SRC_ALPHA,
            GL_ONE_MINUS_SRC_ALPHA
        )

        glDisable(GL_LIGHTING)

        for p in self.particles:

            r, g, b = p.color
            s = p.size

            glPushMatrix()

            glTranslatef(
                p.x,
                p.y,
                p.z
            )

            # ukuran lampion
            glScalef(
                s,
                s * 1.8,
                s
            )

            # ==================================================
            # BADAN LAMPION
            # ==================================================
            glBegin(GL_QUADS)

            # DEPAN
            glColor4f(r, g, b, p.alpha)

            glVertex3f(-0.22, -0.35, 0.22)
            glVertex3f( 0.22, -0.35, 0.22)

            glColor4f(
                r * 0.35,
                g * 0.25,
                b * 0.18,
                p.alpha
            )

            glVertex3f( 0.22, 0.35, 0.22)
            glVertex3f(-0.22, 0.35, 0.22)

            # BELAKANG
            glColor4f(r, g, b, p.alpha)

            glVertex3f(-0.22, -0.35, -0.22)
            glVertex3f( 0.22, -0.35, -0.22)

            glColor4f(
                r * 0.35,
                g * 0.25,
                b * 0.18,
                p.alpha
            )

            glVertex3f( 0.22, 0.35, -0.22)
            glVertex3f(-0.22, 0.35, -0.22)

            # KIRI
            glColor4f(
                r * 0.9,
                g * 0.9,
                b * 0.9,
                p.alpha
            )

            glVertex3f(-0.22, -0.35, -0.22)
            glVertex3f(-0.22, -0.35,  0.22)

            glColor4f(
                r * 0.30,
                g * 0.20,
                b * 0.15,
                p.alpha
            )

            glVertex3f(-0.22, 0.35,  0.22)
            glVertex3f(-0.22, 0.35, -0.22)

            # KANAN
            glColor4f(
                r * 0.9,
                g * 0.9,
                b * 0.9,
                p.alpha
            )

            glVertex3f(0.22, -0.35, -0.22)
            glVertex3f(0.22, -0.35,  0.22)

            glColor4f(
                r * 0.30,
                g * 0.20,
                b * 0.15,
                p.alpha
            )

            glVertex3f(0.22, 0.35,  0.22)
            glVertex3f(0.22, 0.35, -0.22)

            # ATAS
            glColor4f(
                r * 0.20,
                g * 0.14,
                b * 0.10,
                p.alpha
            )

            glVertex3f(-0.22, 0.35, -0.22)
            glVertex3f(-0.22, 0.35,  0.22)
            glVertex3f( 0.22, 0.35,  0.22)
            glVertex3f( 0.22, 0.35, -0.22)

            glEnd()

            # ==================================================
            # RING BAWAH
            # ==================================================
            glColor4f(
                0.22,
                0.15,
                0.08,
                p.alpha
            )

            glBegin(GL_LINE_LOOP)

            glVertex3f(-0.22, -0.35, -0.22)
            glVertex3f(-0.22, -0.35,  0.22)
            glVertex3f( 0.22, -0.35,  0.22)
            glVertex3f( 0.22, -0.35, -0.22)

            glEnd()

            # ==================================================
            # API
            # ==================================================
            glPushMatrix()

            glTranslatef(
                0,
                -0.30,
                0
            )

            glColor4f(
                1.0,
                0.85,
                0.25,
                p.alpha
            )

            gluSphere(
                q,
                0.05,
                10,
                10
            )

            glPopMatrix()

            # ==================================================
            # GLOW BAWAH
            # ==================================================
            glEnable(GL_BLEND)

            glBlendFunc(
                GL_SRC_ALPHA,
                GL_ONE
            )

            glPushMatrix()

            glTranslatef(
                0,
                -0.28,
                0
            )

            glColor4f(
                1.0,
                0.70,
                0.20,
                p.alpha * 0.14
            )

            gluSphere(
                q,
                0.22,
                12,
                12
            )

            glPopMatrix()

            glBlendFunc(
                GL_SRC_ALPHA,
                GL_ONE_MINUS_SRC_ALPHA
            )

            glPopMatrix()

        glDisable(GL_BLEND)