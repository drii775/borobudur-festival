from OpenGL.GL import *
from OpenGL.GLU import *


# ─────────────────────────────────────────────
#  TANAH & BINTANG
# ─────────────────────────────────────────────
def draw_ground():
    glDisable(GL_LIGHTING)
    glColor3f(0.08, 0.14, 0.06)
    glBegin(GL_QUADS)
    glVertex3f(-80, -0.02, -80)
    glVertex3f(80, -0.02, -80)
    glVertex3f(80, -0.02, 80)
    glVertex3f(-80, -0.02, 80)
    glEnd()


def draw_stars(stars):
    glDisable(GL_LIGHTING)
    glPointSize(1.8)
    glBegin(GL_POINTS)
    for x, y, z, b in stars:
        glColor3f(b, b, min(1.0, b * 1.1))
        glVertex3f(x, y, z)
    glEnd()
    glPointSize(1.0)
