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

    # =========================
    # CYLINDER STUPA L1
    # =========================

    radius_base = 2
    radius_shrink = 0.2

    cylinder_height = 0.1

    for i in range(2):

        radius = radius_base - (i * radius_shrink)

        glColor3f(0.70, 0.66, 0.60)

        glPushMatrix()

        glTranslatef(0, current_top, 0)

        glRotatef(-90, 1, 0, 0)

        gluCylinder(
            quadric,
            radius,
            radius,
            cylinder_height,
            64,
            2,
        )

        gluDisk(quadric, 0, radius, 64, 1)

        glTranslatef(0, 0, cylinder_height)

        gluDisk(quadric, 0, radius, 64, 1)

        glPopMatrix()

        current_top += cylinder_height

    # =========================
    # CYLINDER STUPA L2
    # =========================

    radius_base = 1.7
    radius_shrink = 0.05

    cylinder_height = 0.05

    for i in range(2):

        radius = radius_base - (i * radius_shrink)

        glColor3f(0.76, 0.72, 0.65)

        glPushMatrix()

        glTranslatef(0, current_top, 0)

        glRotatef(-90, 1, 0, 0)

        gluCylinder(
            quadric,
            radius,
            radius,
            cylinder_height,
            64,
            2,
        )

        gluDisk(quadric, 0, radius, 64, 1)

        glTranslatef(0, 0, cylinder_height)

        gluDisk(quadric, 0, radius, 64, 1)

        glPopMatrix()

        current_top += cylinder_height

    # =========================
    # STUPA UTAMA
    # =========================

    # body stupa
    body_radius = 1.6
    body_h = 1.0

    glColor3f(0.72, 0.68, 0.60)

    glPushMatrix()

    glTranslatef(0, current_top, 0)
    glRotatef(-90, 1, 0, 0)

    gluCylinder(
        quadric,
        body_radius,
        body_radius,
        body_h,
        64,
        4,
    )

    gluDisk(
        quadric,
        0,
        body_radius,
        64,
        1,
    )

    glTranslatef(0, 0, body_h)

    gluDisk(
        quadric,
        0,
        body_radius,
        64,
        1,
    )

    glPopMatrix()

    current_top += body_h

    # # =========================
    # # HEMISPHERE
    # # =========================

    sphere_radius = 1.15

    glColor3f(0.78, 0.74, 0.66)

    glPushMatrix()

    glTranslatef(0, current_top, 0)

    # gepeng hemisphere
    glScalef(
        sphere_radius * 1.4,
        sphere_radius * 0.4,
        sphere_radius * 1.4,
    )

    gluSphere(
        quadric,
        1,
        32,
        16,
    )

    glPopMatrix()

    current_top += sphere_radius * 0.4

    # # =========================
    # # HARMIKA
    # # =========================

    harmika_h = 0.2

    glColor3f(0.60, 0.58, 0.54)

    glPushMatrix()

    glTranslatef(
        0,
        current_top + harmika_h / 2,
        0,
    )

    glScalef(0.9, harmika_h, 0.9)

    draw_box()

    glPopMatrix()

    current_top += harmika_h

    # # =========================
    # # PUNCAK
    # # =========================

    cone_h = 1.5
    cone_radius = 0.4

    glColor3f(0.85, 0.78, 0.62)

    glPushMatrix()

    glTranslatef(0, current_top, 0)

    glRotatef(-90, 1, 0, 0)

    gluCylinder(
        quadric,
        cone_radius,
        0.25,
        cone_h,
        32,
        4,
    )

    glPopMatrix()

    glPopMatrix()
