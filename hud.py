from OpenGL.GL import *
from OpenGL.GLU import *

from config import *

import pygame


# ─────────────────────────────────────────────
#  HUD — render teks sebagai texture quad
#  (glDrawPixels tidak didukung di MacOS modern)
# ─────────────────────────────────────────────
def render_hud_texture(hud_surf, font_sm, font_lg, ps, paused, fps):
    hud_surf.fill((0, 0, 0, 0))

    # Judul
    s = font_lg.render("Festival Lampion Borobudur", True, (255, 215, 80))
    hud_surf.blit(s, (14, 10))

    # Info panel
    lines = [
        f"Lampion aktif : {len(ps.particles)}",
        f"Maks lampion  : {ps.max_p}",
        f"FPS           : {fps:.0f}",
        f"Status        : {'PAUSED' if paused else 'RUNNING'}",
    ]
    for i, ln in enumerate(lines):
        hud_surf.blit(font_sm.render(ln, True, (200, 200, 180)), (14, 48 + i * 22))

    # Kontrol (pojok kiri bawah)
    ctrl = [
        "[ KONTROL ]",
        "Drag    → Rotasi kamera",
        "Scroll  → Zoom",
        "SPACE   → Pause / lanjut",
        "+  /  - → Jumlah lampion",
        "R       → Reset kamera",
        "ESC / Q → Keluar",
    ]
    y0 = WINDOW_H - len(ctrl) * 21 - 12
    for i, ln in enumerate(ctrl):
        col = (255, 215, 80) if i == 0 else (150, 150, 130)
        hud_surf.blit(font_sm.render(ln, True, col), (14, y0 + i * 21))


def draw_hud_quad(hud_surf):
    """Upload hud_surf sebagai OpenGL texture, gambar sebagai fullscreen quad."""
    tex_data = pygame.image.tostring(hud_surf, "RGBA", True)

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGBA,
        WINDOW_W,
        WINDOW_H,
        0,
        GL_RGBA,
        GL_UNSIGNED_BYTE,
        tex_data,
    )

    # Switch ke proyeksi ortho 2D
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, WINDOW_W, 0, WINDOW_H, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(1, 1, 1, 1)

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(0, 0)
    glTexCoord2f(1, 0)
    glVertex2f(WINDOW_W, 0)
    glTexCoord2f(1, 1)
    glVertex2f(WINDOW_W, WINDOW_H)
    glTexCoord2f(0, 1)
    glVertex2f(0, WINDOW_H)
    glEnd()

    glDisable(GL_TEXTURE_2D)
    glDisable(GL_BLEND)
    glEnable(GL_DEPTH_TEST)

    # Restore matrices
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

    glDeleteTextures([tex_id])
