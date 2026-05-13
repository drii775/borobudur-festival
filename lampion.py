from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math

# ==================================================
# KONFIGURASI
# ==================================================
MAX_PARTICLES = 260
SPAWN_RATE = 3

PARTICLE_MIN_Y = 1.0
PARTICLE_MAX_Y = 90.0


# ==================================================
# KELAS PARTIKEL LAMPION
# ==================================================
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

        # ==================================================
        # AREA SPAWN
        # ==================================================
        spawn_type = random.randint(0, 1)

        # ==================================================
        # AREA CANDI
        # ==================================================
        if spawn_type == 0:

            self.x = random.uniform(-12, 12)
            self.z = random.uniform(-12, 12)

        # ==================================================
        # AREA TANAH
        # ==================================================
        else:

            side = random.randint(0, 3)

            if side == 0:

                self.x = random.uniform(-38, -18)
                self.z = random.uniform(-38, 38)

            elif side == 1:

                self.x = random.uniform(18, 38)
                self.z = random.uniform(-38, 38)

            elif side == 2:

                self.x = random.uniform(-38, 38)
                self.z = random.uniform(-38, -18)

            else:

                self.x = random.uniform(-38, 38)
                self.z = random.uniform(18, 38)

        # tinggi awal
        self.y = (
            PARTICLE_MIN_Y +
            random.uniform(-1.0, 2.0)
        )

        # ==================================================
        # GERAKAN
        # ==================================================
        self.vy = random.uniform(0.07, 0.16)

        self.vx = random.uniform(-0.035, 0.035)
        self.vz = random.uniform(-0.035, 0.035)

        # ==================================================
        # EFEK ANGIN
        # ==================================================
        self.osc_amp = random.uniform(0.03, 0.12)

        self.osc_speed = random.uniform(0.3, 6.0)

        self.osc_phase = random.uniform(
            0,
            2 * math.pi
        )

        # ==================================================
        # VISUAL
        # ==================================================
        self.color = random.choice(
            self.COLOR_PALETTE
        )

        self.size = random.uniform(
            0.55,
            1.05
        )

        self.age = 0

        self.life = random.uniform(
            260,
            520
        )

        self.alpha = 0.0

    def update(self, time):

        self.age += 1

        # gerakan naik
        self.y += self.vy

        # gerakan angin X
        self.x += (
            self.vx +
            math.sin(
                time *
                self.osc_speed +
                self.osc_phase
            ) * self.osc_amp
        )

        # gerakan angin Z
        self.z += (
            self.vz +
            math.cos(
                time *
                self.osc_speed +
                self.osc_phase
            ) * self.osc_amp * 0.5
        )

        # fade
        fade = 35

        if self.age < fade:

            self.alpha = (
                self.age / fade
            )

        elif self.age > self.life - fade:

            self.alpha = (
                (self.life - self.age) / fade
            )

        else:

            self.alpha = 1.0

        self.alpha = max(
            0.0,
            min(1.0, self.alpha)
        )

        return (
            self.y > PARTICLE_MAX_Y
            or self.age >= self.life
        )


# ==================================================
# SISTEM PARTIKEL
# ==================================================
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

        # spawn random
        spawn_random = random.randint(
            1,
            SPAWN_RATE
        )

        need = min(
            spawn_random,
            self.max_p - len(self.particles)
        )

        for _ in range(need):

            if random.random() > 0.15:

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

            # ==================================================
            # UKURAN BERDASARKAN JARAK
            # ==================================================
            camera_distance = math.sqrt(
                (p.x * p.x) +
                (p.y * p.y) +
                (p.z * p.z)
            )

            distance_scale = max(
                0.45,
                1.4 - (
                    camera_distance / 60.0
                )
            )

            s = p.size * distance_scale

            glPushMatrix()

            glTranslatef(
                p.x,
                p.y,
                p.z
            )

            # ==================================================
            # GOYANGAN ANGIN
            # ==================================================
            glRotatef(
                math.sin(
                    self.time *
                    p.osc_speed
                ) * 12,
                0,
                0,
                1
            )

            glRotatef(
                math.cos(
                    self.time *
                    p.osc_speed
                ) * 8,
                1,
                0,
                0
            )

            # ==================================================
            # SKALA
            # ==================================================
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
            glColor4f(
                r,
                g,
                b,
                p.alpha
            )

            glVertex3f(
                -0.22,
                -0.35,
                 0.22
            )

            glVertex3f(
                 0.22,
                -0.35,
                 0.22
            )

            glColor4f(
                r * 0.35,
                g * 0.25,
                b * 0.18,
                p.alpha
            )

            glVertex3f(
                 0.22,
                 0.35,
                 0.22
            )

            glVertex3f(
                -0.22,
                 0.35,
                 0.22
            )

            # BELAKANG
            glColor4f(
                r,
                g,
                b,
                p.alpha
            )

            glVertex3f(
                -0.22,
                -0.35,
                -0.22
            )

            glVertex3f(
                 0.22,
                -0.35,
                -0.22
            )

            glColor4f(
                r * 0.35,
                g * 0.25,
                b * 0.18,
                p.alpha
            )

            glVertex3f(
                 0.22,
                 0.35,
                -0.22
            )

            glVertex3f(
                -0.22,
                 0.35,
                -0.22
            )

            # KIRI
            glColor4f(
                r * 0.9,
                g * 0.9,
                b * 0.9,
                p.alpha
            )

            glVertex3f(
                -0.22,
                -0.35,
                -0.22
            )

            glVertex3f(
                -0.22,
                -0.35,
                 0.22
            )

            glColor4f(
                r * 0.30,
                g * 0.20,
                b * 0.15,
                p.alpha
            )

            glVertex3f(
                -0.22,
                 0.35,
                 0.22
            )

            glVertex3f(
                -0.22,
                 0.35,
                -0.22
            )

            # KANAN
            glColor4f(
                r * 0.9,
                g * 0.9,
                b * 0.9,
                p.alpha
            )

            glVertex3f(
                 0.22,
                -0.35,
                -0.22
            )

            glVertex3f(
                 0.22,
                -0.35,
                 0.22
            )

            glColor4f(
                r * 0.30,
                g * 0.20,
                b * 0.15,
                p.alpha
            )

            glVertex3f(
                 0.22,
                 0.35,
                 0.22
            )

            glVertex3f(
                 0.22,
                 0.35,
                -0.22
            )

            # ATAS
            glColor4f(
                r * 0.18,
                g * 0.12,
                b * 0.08,
                p.alpha
            )

            glVertex3f(
                -0.22,
                 0.35,
                -0.22
            )

            glVertex3f(
                -0.22,
                 0.35,
                 0.22
            )

            glVertex3f(
                 0.22,
                 0.35,
                 0.22
            )

            glVertex3f(
                 0.22,
                 0.35,
                -0.22
            )

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

            glVertex3f(
                -0.22,
                -0.35,
                -0.22
            )

            glVertex3f(
                -0.22,
                -0.35,
                 0.22
            )

            glVertex3f(
                 0.22,
                -0.35,
                 0.22
            )

            glVertex3f(
                 0.22,
                -0.35,
                -0.22
            )

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
                0.06,
                12,
                12
            )

            glPopMatrix()

            glPopMatrix()

        glEnable(GL_LIGHTING)

        glDisable(GL_BLEND)