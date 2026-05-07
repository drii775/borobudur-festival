import math

from OpenGL.GL import *
from OpenGL.GLU import *


def draw_box():
    v = [
        [-0.5, -0.5, -0.5],
        [0.5, -0.5, -0.5],
        [0.5, 0.5, -0.5],
        [-0.5, 0.5, -0.5],
        [-0.5, -0.5, 0.5],
        [0.5, -0.5, 0.5],
        [0.5, 0.5, 0.5],
        [-0.5, 0.5, 0.5],
    ]
    faces = [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [0, 1, 5, 4],
        [2, 3, 7, 6],
        [0, 3, 7, 4],
        [1, 2, 6, 5],
    ]
    normals = [[0, 0, -1], [0, 0, 1], [0, -1, 0], [0, 1, 0], [-1, 0, 0], [1, 0, 0]]
    glBegin(GL_QUADS)
    for fi, face in enumerate(faces):
        glNormal3fv(normals[fi])
        for vi in face:
            glVertex3fv(v[vi])
    glEnd()


def draw_borobudur(quadric):
    SC = (0.44, 0.40, 0.34)
    SD = (0.30, 0.27, 0.22)
    SA = (0.58, 0.53, 0.44)

    glPushMatrix()

    glScalef(2.5, 2.5, 2.5)

    # Platform dasar
    # glColor3f(*SD)
    # glPushMatrix()
    # glTranslatef(0, 0.25, 0)
    # glScalef(22, 0.5, 22)
    # draw_box()
    # glPopMatrix()

    # =========================
    # BOROBUDUR BASE
    # =========================

    STONE = (0.55, 0.52, 0.48)
    STONE_DARK = (0.38, 0.35, 0.30)

    # kaki
    foot_h = 0.4

    glColor3f(*STONE_DARK)

    glPushMatrix()
    glTranslatef(0, foot_h / 2, 0)
    glScalef(30, foot_h, 30)
    draw_box()
    glPopMatrix()

    current_top = foot_h

    # # 6 teras persegi
    # tiers = [
    #     (15, 1, 15),
    #     (13, 1, 13),
    #     (11, 1, 11),
    #     (9.5, 1, 9.5),
    #     (8, 1, 8),
    #     (6.5, 1, 6.5),
    # ]
    # yo = 0.5
    # for i, (sx, sy, sz) in enumerate(tiers):
    #     t = i / len(tiers)
    #     rc = SC[0] + t * 0.06
    #     gc = SC[1] + t * 0.05
    #     bc = SC[2] + t * 0.04
    #     glColor3f(rc, gc, bc)
    #     glPushMatrix()
    #     glTranslatef(0, yo + sy / 2, 0)
    #     glScalef(sx, sy, sz)
    #     draw_box()
    #     glPopMatrix()

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
    radius_shrink = 0.8

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

    #     # Ornamen sudut
    #     glColor3f(*SA)
    #     for dx in [-sx / 2 + 0.4, sx / 2 - 0.4]:
    #         for dz in [-sz / 2 + 0.4, sz / 2 - 0.4]:
    #             glPushMatrix()
    #             glTranslatef(dx, yo + sy, dz)
    #             gluCylinder(quadric, 0.15, 0.10, 0.35, 6, 2)
    #             glPopMatrix()
    #     yo += sy

    # # 3 teras lingkaran
    # circ = [(5.8, 0.8, 16), (4.4, 0.8, 12), (3.1, 0.8, 8)]
    # for ro, h, ns in circ:
    #     ri = ro - 0.85
    #     glColor3f(*SC)
    #     glPushMatrix()
    #     glTranslatef(0, yo, 0)
    #     gluCylinder(q, ro, ro, h, 32, 2)
    #     gluCylinder(q, ri, ri, h, 32, 2)
    #     glTranslatef(0, 0, h)
    #     gluDisk(q, ri, ro, 32, 3)
    #     glPopMatrix()
    #     glPushMatrix()
    #     glTranslatef(0, yo, 0)
    #     gluDisk(q, ri, ro, 32, 3)
    #     glPopMatrix()

    #     # Stupa kecil
    #     glColor3f(*SA)
    #     sr = (ro + ri) / 2
    #     for j in range(ns):
    #         ang = j / ns * 2 * math.pi
    #         sx_ = sr * math.cos(ang)
    #         sz_ = sr * math.sin(ang)
    #         glPushMatrix()
    #         glTranslatef(sx_, yo + h, sz_)
    #         gluCylinder(q, 0.20, 0.20, 0.30, 8, 2)
    #         glTranslatef(0, 0.30, 0)
    #         gluSphere(q, 0.26, 8, 6)
    #         glTranslatef(0, 0.22, 0)
    #         gluCylinder(q, 0.05, 0, 0.25, 6, 2)
    #         glPopMatrix()
    #     yo += h

    # # Stupa utama
    # glColor3f(0.66, 0.61, 0.52)
    # glPushMatrix()
    # glTranslatef(0, yo, 0)
    # gluCylinder(q, 1.25, 1.05, 1.60, 16, 4)
    # glTranslatef(0, 1.60, 0)
    # glColor3f(0.72, 0.67, 0.57)
    # gluSphere(q, 1.35, 20, 16)
    # glColor3f(0.82, 0.77, 0.62)
    # glTranslatef(0, 0.85, 0)
    # gluDisk(q, 0, 0.50, 12, 2)
    # glTranslatef(0, 0.10, 0)
    # gluSphere(q, 0.46, 12, 10)
    # glColor3f(0.92, 0.87, 0.72)
    # glTranslatef(0, 0.50, 0)
    # gluCylinder(q, 0.14, 0, 1.10, 8, 4)
    # glPopMatrix()

    glPopMatrix()
