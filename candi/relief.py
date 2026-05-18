from OpenGL.GL import *
from candi.stupa import *


def draw_relief_corner(size=18, y=0, layer_h=0.8):

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
        (0.85, 0.1, 0.3, 1.5, 0.34),
        (0.75, 0.1, 0.25, 0.2, 0.50),
        (0.57, 0.1, 0.15, 0.8, 0.38),
        (0.41, 0.1, 0.18, 0.43, 0.34),
        (0.25, 0.1, 0.15, 0.2, 0.38),
        (0.09, 0.1, 0.18, 0.43, 0.42),
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

            glColor3f(c, c, c + 0.02)

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

    ornament_count = 7

    spacing = relief_len / ornament_count

    start_x = seg_x - (relief_len / 2) + (spacing / 2)

    for i in range(ornament_count):

        x = start_x + (i * spacing)

        # =====================================
        # LIS BAWAH
        # =====================================

        glColor3f(0.42, 0.42, 0.45)

        glPushMatrix()

        glTranslatef(
            x,
            y + 0.01,
            (size / 2) + 0.12,
        )

        glScalef(
            spacing * 0.95,
            0.06,
            0.3,
        )

        draw_box()

        glPopMatrix()

        # =====================================
        # TIANG KIRI
        # =====================================

        glColor3f(0.50, 0.50, 0.52)

        glPushMatrix()

        glTranslatef(
            x - (spacing * 0.2),
            y + 0.2,
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
            y + 0.2,
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
            y + 0.38,
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

        glColor3f(0.58, 0.58, 0.60)

        # kaki duduk
        glPushMatrix()

        glTranslatef(
            x,
            y + 0.11,
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
            y + 0.19,
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
            y + 0.26,
            (size / 2) + 0.01,
        )

        gluSphere(
            quadric,
            0.022,
            10,
            10,
        )

        glPopMatrix()

        # =====================================
        # STUPA MINI
        # =====================================
        glPushMatrix()

        glTranslatef(
            x,
            y + 0.42,
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
