import math

from OpenGL.GL import *
from OpenGL.GLU import *

from stupa import draw_box, draw_stupa


def draw_borobudur(quadric):
    SC = (0.44, 0.40, 0.34)
    SD = (0.30, 0.27, 0.22)
    SA = (0.58, 0.53, 0.44)

    glPushMatrix()

    glScalef(2.5, 2.5, 2.5)

    # =========================
    # BOROBUDUR BASE
    # =========================

    STONE = (0.42, 0.39, 0.35)
    STONE_DARK = (0.32, 0.30, 0.28)

    # kaki
    foot_h = 0.4

    glColor3f(*STONE_DARK)

    glPushMatrix()
    glTranslatef(0, foot_h / 2, 0)
    glScalef(30, foot_h, 30)
    draw_box()
    glPopMatrix()

    current_top = foot_h

    # =========================
    # 5 tingkat persegi
    # =========================

    base_size = 18
    shrink = 1.6
    cube_h = 1.2

    for i in range(5):

        size = base_size - (i * shrink)

        current_y = current_top + cube_h / 2

        t = i / 5.0

        glColor3f(
            STONE[0] + t * 0.08,
            STONE[1] + t * 0.07,
            STONE[2] + t * 0.06,
        )

        glPushMatrix()

        glTranslatef(0, current_y, 0)
        glScalef(size, cube_h, size)

        draw_box()

        glPopMatrix()

        current_top += cube_h

    # =========================
    # 3 tingkat melingkar
    # =========================

    radius_base = 5
    radius_shrink = 1

    cylinder_height = 0.4

    for i in range(3):

        radius = radius_base - (i * radius_shrink)

        current_y = current_top

        glColor3f(0.62, 0.58, 0.52)

        glPushMatrix()

        # posisi bawah cylinder
        glTranslatef(0, current_y, 0)

        # putar agar berdiri
        glRotatef(-90, 1, 0, 0)

        # body cylinder
        gluCylinder(
            quadric,
            radius,
            radius,
            cylinder_height,
            64,
            4,
        )

        # tutup bawah
        gluDisk(
            quadric,
            0,
            radius,
            64,
            1,
        )

        # tutup atas
        glTranslatef(0, 0, cylinder_height)

        gluDisk(
            quadric,
            0,
            radius,
            64,
            1,
        )

        glPopMatrix()

        current_top += cylinder_height

    # =========================
    # STUPA KECIL MELINGKAR
    # =========================

    layers = [
        (16, 4.5),
        (12, 3.5),
        (8, 2.5),
    ]

    base_y = current_top - (2 * cylinder_height)

    for layer_idx, (count, ring_radius) in enumerate(layers):

        layer_y = base_y + (layer_idx * cylinder_height)

        for i in range(count):

            angle = (2 * math.pi * i) / count

            x = math.cos(angle) * ring_radius
            z = math.sin(angle) * ring_radius

            glPushMatrix()

            glTranslatef(x, layer_y, z)

            draw_stupa(quadric, scale=0.2)

            glPopMatrix()

    # =========================
    # STUPA UTAMA
    # =========================

    glPushMatrix()

    glTranslatef(0, current_top, 0)

    draw_stupa(quadric, scale=0.8)

    glPopMatrix()

    glPopMatrix()
