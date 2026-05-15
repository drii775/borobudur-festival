from OpenGL.GL import *
from candi.stupa import draw_box


def draw_stairs(scale=1.0):

    step_w = 1 * scale
    step_h = 0.09 * scale
    step_d = 0.08 * scale

    steps = 9

    wall_w = 0.15 * scale
    wall_h = steps * step_h - 0.02

    # =========================
    # ANAK TANGGA
    # =========================

    for i in range(steps):

        y = i * step_h
        z = -(i * step_d)

        glColor3f(0.50, 0.48, 0.46)

        glPushMatrix()

        glTranslatef(0, y, z)

        glScalef(
            step_w,
            step_h,
            step_d,
        )

        draw_box()

        glPopMatrix()

    # =========================
    # DINDING KIRI
    # =========================

    glColor3f(0.36, 0.34, 0.32)

    glPushMatrix()

    glTranslatef(
        -(step_w / 2),
        wall_h / 2,
        -((steps - 1) * step_d) / 2,
    )

    glScalef(
        wall_w,
        wall_h,
        steps * step_d,
    )

    draw_box()

    glPopMatrix()

    # =========================
    # DINDING KANAN
    # =========================

    glPushMatrix()

    glTranslatef(
        (step_w / 2),
        wall_h / 2,
        -((steps - 1) * step_d) / 2,
    )

    glScalef(
        wall_w,
        wall_h,
        steps * step_d,
    )

    draw_box()

    glPopMatrix()
