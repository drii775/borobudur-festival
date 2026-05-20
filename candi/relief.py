from OpenGL.GL import *
from candi.stupa import *


def draw_relief_corner(size=18, y=0, layer_h=0.8, show_upper=False):

    # =========================
    # UKURAN
    # =========================

    lower_h = layer_h
    lower_d = 0.22

    relief_len = (size / 2) - 0.42

    # =========================
    # DETAIL UKIRAN
    # =========================

    details = [
        # y_offset, z_offset, scale_y, scale_z, color
        (0.75, 0.1, 0.5, 1.5, 0.46),
        (0.5, 0.1, 0.25, 0.8, 0.52),
        (0.05, 0.1, 0.7, 0.43, 0.58),
    ]

    # =========================
    # LOOP 4 SISI
    # =========================

    segments = [
        -(size / 4) - 0.22,
        (size / 4) + 0.22,
    ]

    for seg_x in segments:

        # =========================
        # RELIEF BAWAH
        # =========================

        for y_off, z_off, sy, sz, c in details:

            glColor3f(c + 0.05, c + 0.03, c)

            # =========================
            # PANJANG KHUSUS SUDUT
            # =========================

            extra_len = 0.07 + (0.135 * sz)

            if seg_x < 0:
                detail_x = seg_x - (extra_len / 2)
            else:
                detail_x = seg_x + (extra_len / 2)

            # =========================
            # DETAIL RELIEF
            # =========================

            glPushMatrix()

            glTranslatef(
                detail_x,
                y + (lower_h * y_off),
                (size / 2) + z_off + 0.003,
            )

            glScalef(
                relief_len + extra_len,
                lower_h * sy,
                lower_d * sz,
            )

            draw_box()

            glPopMatrix()

        # =========================
        # RELIEF ATAS
        # =========================

        if show_upper:
            draw_upper_ornament(
                size=size,
                y=y + lower_h,
                lower_h=lower_h,
                seg_x=seg_x,
                relief_len=relief_len,
            )


# ==================================================
# ORNAMEN ATAS BOROBUDUR
# ==================================================


def draw_upper_ornament(
    size,
    y,
    lower_h,
    seg_x,
    relief_len,
):

    ornament_count = 4

    spacing = relief_len / ornament_count

    start_x = seg_x - (relief_len / 2) + (spacing / 2)

    for i in range(ornament_count):

        x = start_x + (i * spacing)
        # =====================================
        # TIANG KIRI
        # =====================================

        glColor3f(0.62, 0.58, 0.52)

        glPushMatrix()

        glTranslatef(
            x - (spacing * 0.2),
            y + 0.15,
            (size / 2) + 0.12,
        )

        glScalef(
            0.1,
            0.32,
            0.28,
        )

        draw_box()

        glPopMatrix()

        # =====================================
        # TIANG KANAN
        # =====================================

        glPushMatrix()

        glTranslatef(
            x + (spacing * 0.2),
            y + 0.15,
            (size / 2) + 0.12,
        )

        glScalef(
            0.1,
            0.32,
            0.28,
        )

        draw_box()

        glPopMatrix()

        # =====================================
        # BALOK ATAS
        # =====================================

        glPushMatrix()

        glTranslatef(
            x,
            y + 0.35,
            (size / 2) + 0.12,
        )

        glScalef(
            spacing * 0.5,
            0.08,
            0.3,
        )

        draw_box()

        glPopMatrix()

        # =====================================
        # PATUNG BUDDHA
        # =====================================

        glColor3f(0.72, 0.68, 0.60)

        # kaki duduk
        glPushMatrix()

        glTranslatef(
            x,
            y + 0.02,
            (size / 2) + 0.01,
        )

        glScalef(
            0.16,
            0.05,
            0.12,
        )

        draw_box()

        glPopMatrix()

        # badan
        glPushMatrix()

        glTranslatef(
            x,
            y + 0.1,
            (size / 2) + 0.01,
        )

        glScalef(
            0.09,
            0.11,
            0.07,
        )

        draw_box()

        glPopMatrix()

        # kepala
        quadric = gluNewQuadric()

        glPushMatrix()

        glTranslatef(
            x,
            y + 0.17,
            (size / 2) + 0.01,
        )

        gluSphere(
            quadric,
            0.022,
            6,
            6,
        )

        glPopMatrix()

        # =====================================
        # STUPA MINI
        # =====================================
        glPushMatrix()

        glTranslatef(
            x,
            y + 0.38,
            (size / 2) + 0.12,
        )

        glScalef(
            0.03,
            0.03,
            0.03,
        )

        draw_stupa(
            quadric,
            scale=2.5,
            small=True,
        )

        glPopMatrix()
