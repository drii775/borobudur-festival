from OpenGL.GL import *
from OpenGL.GLU import *

# STUPA_BIG = (0.78, 0.74, 0.66)
# STUPA_SMALL = (0.40, 0.38, 0.35)


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


def draw_stupa(q, scale=1.0, small=False):
    STUPA_BIG = (0.78, 0.74, 0.66)
    STUPA_SMALL = (0.62, 0.58, 0.52)

    # =========================
    # cylinder stupa l1
    # =========================

    radius_base = 2 * scale
    radius_shrink = 0.2 * scale

    cylinder_height = 0.1 * scale

    current_top = 0

    for i in range(3):

        radius = radius_base - (i * radius_shrink)

        glColor3f(0.70, 0.66, 0.60)

        glPushMatrix()

        glTranslatef(0, current_top, 0)

        glRotatef(-90, 1, 0, 0)

        gluCylinder(
            q,
            radius,
            radius,
            cylinder_height,
            32,
            2,
        )

        gluDisk(q, 0, radius, 32, 1)

        glTranslatef(0, 0, cylinder_height)

        gluDisk(q, 0, radius, 32, 1)

        glPopMatrix()

        current_top += cylinder_height

    # =========================
    # cylinder stupa l2
    # =========================

    radius_base = 1.7 * scale
    radius_shrink = 0.05 * scale

    cylinder_height = 0.05 * scale

    for i in range(3):

        radius = radius_base - (i * radius_shrink)

        glColor3f(0.76, 0.72, 0.65)

        glPushMatrix()

        glTranslatef(0, current_top, 0)

        glRotatef(-90, 1, 0, 0)

        gluCylinder(
            q,
            radius,
            radius,
            cylinder_height,
            32,
            2,
        )

        gluDisk(q, 0, radius, 32, 1)

        glTranslatef(0, 0, cylinder_height)

        gluDisk(q, 0, radius, 32, 1)

        glPopMatrix()

        current_top += cylinder_height

    # =========================
    # body stupa
    # =========================

    body_radius = 1.6 * scale
    body_h = 1.0 * scale

    glColor3f(0.72, 0.68, 0.60)

    glPushMatrix()

    glTranslatef(0, current_top, 0)
    glRotatef(-90, 1, 0, 0)

    gluCylinder(q, body_radius, body_radius, body_h, 32, 4)

    gluDisk(q, 0, body_radius, 32, 1)

    glTranslatef(0, 0, body_h)

    gluDisk(q, 0, body_radius, 32, 1)

    glPopMatrix()

    current_top += body_h

    # =========================
    # hemisphere
    # =========================

    sphere_radius = 1.15 * scale

    if small:
        glColor3f(*STUPA_SMALL)
    else:
        glColor3f(*STUPA_BIG)

    glPushMatrix()

    glTranslatef(0, current_top, 0)

    glScalef(
        sphere_radius * 1.4,
        sphere_radius * 0.4,
        sphere_radius * 1.4,
    )

    gluSphere(q, 1, 48, 32)

    glPopMatrix()

    current_top += sphere_radius * 0.4

    # =========================
    # harmika
    # =========================

    harmika_h = 0.2 * scale

    if small:
        glColor3f(0.45, 0.43, 0.40)
    else:
        glColor3f(0.40, 0.38, 0.35)

    glPushMatrix()

    glTranslatef(
        0,
        current_top + harmika_h / 2,
        0,
    )

    glScalef(
        0.9 * scale,
        harmika_h,
        0.9 * scale,
    )

    draw_box()

    glPopMatrix()

    current_top += harmika_h

    # =========================
    # cone
    # =========================

    cone_h = 1.2 * scale
    cone_radius = 0.4 * scale

    glColor3f(0.85, 0.82, 0.72)

    glPushMatrix()

    glTranslatef(0, current_top, 0)

    glRotatef(-90, 1, 0, 0)

    gluCylinder(
        q,
        cone_radius,
        0.25 * scale,
        cone_h,
        16,
        4,
    )

    glPopMatrix()
