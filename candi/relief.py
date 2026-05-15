from OpenGL.GL import *
from candi.stupa import draw_box


def draw_relief_corner(size=18, y=0, layer_h=0.8):

    # =========================
    # UKURAN
    # =========================

    lower_h = layer_h
    lower_d = 0.22

    upper_h = lower_h * 0.5
    upper_d = 0.35

    relief_len = (size / 2) - 0.42

    # =========================
    # DETAIL UKIRAN
    # =========================

    details = [
        # y_offset, z_offset, scale_y, scale_z, color
        (0.85, 0.08, 0.3, 1, 0.34),
        (0.75, 0.08, 0.25, 0.2, 0.50),
        (0.57, 0.08, 0.15, 0.85, 0.38),
        (0.41, 0.08, 0.18, 0.43, 0.34),
        (0.25, 0.06, 0.15, 0.2, 0.38),
        (0.09, 0.08, 0.18, 0.43, 0.42),
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

            extra_len = 0.04 + (0.145 * sz)

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

        glColor3f(0.48, 0.46, 0.42)

        glPushMatrix()

        glTranslatef(
            seg_x,
            y + lower_h + (upper_h / 2),
            (size / 2) + 0.03,
        )

        glScalef(
            relief_len,
            upper_h,
            upper_d,
        )

        draw_box()

        glPopMatrix()
