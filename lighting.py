from OpenGL.GL import *
from OpenGL.GLU import *


# ─────────────────────────────────────────────
#  PENCAHAYAAN
# ─────────────────────────────────────────────
def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.30, 0.30, 0.35, 1.0])

    glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 18.0, 0.0, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.65, 0.65, 0.70, 1.0])
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.02)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.001)

    glLightfv(GL_LIGHT1, GL_POSITION, [-20.0, 30.0, -10.0, 1.0])
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.30, 0.35, 0.50, 1.0])

    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.35, 0.35, 0.35, 1.0])
