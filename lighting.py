from OpenGL.GL import *
from OpenGL.GLU import *


# ─────────────────────────────────────────────
#  PENCAHAYAAN
# ─────────────────────────────────────────────
def setup_lighting():

    glEnable(GL_LIGHTING)

    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)

    glEnable(GL_COLOR_MATERIAL)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)

    glColorMaterial(
        GL_FRONT_AND_BACK,
        GL_AMBIENT_AND_DIFFUSE
    )

    # ==================================================
    # AMBIENT MALAM
    # ==================================================
    glLightModelfv(
        GL_LIGHT_MODEL_AMBIENT,
        [0.16, 0.16, 0.22, 1.0]
    )

    # ==================================================
    # LIGHT UTAMA BULAN
    # ==================================================
    glLightfv(
        GL_LIGHT0,
        GL_POSITION,
        [0.0, 30.0, 0.0, 1.0]
    )

    glLightfv(
        GL_LIGHT0,
        GL_DIFFUSE,
        [0.45, 0.48, 0.60, 1.0]
    )

    glLightfv(
        GL_LIGHT0,
        GL_SPECULAR,
        [0.20, 0.20, 0.25, 1.0]
    )

    glLightf(
        GL_LIGHT0,
        GL_LINEAR_ATTENUATION,
        0.015
    )

    glLightf(
        GL_LIGHT0,
        GL_QUADRATIC_ATTENUATION,
        0.0005
    )

    # ==================================================
    # LIGHT SAMPING
    # ==================================================
    glLightfv(
        GL_LIGHT1,
        GL_POSITION,
        [-25.0, 20.0, -15.0, 1.0]
    )

    glLightfv(
        GL_LIGHT1,
        GL_DIFFUSE,
        [0.15, 0.18, 0.28, 1.0]
    )

    # ==================================================
    # PANTULAN CAHAYA LAMPION KE CANDI
    # ==================================================
    glLightfv(
        GL_LIGHT2,
        GL_POSITION,
        [0.0, 6.0, 0.0, 1.0]
    )

    glLightfv(
        GL_LIGHT2,
        GL_DIFFUSE,
        [0.40, 0.22, 0.08, 1.0]
    )

    glLightfv(
        GL_LIGHT2,
        GL_SPECULAR,
        [0.10, 0.05, 0.02, 1.0]
    )

    glLightf(
        GL_LIGHT2,
        GL_LINEAR_ATTENUATION,
        0.03
    )

    glLightf(
        GL_LIGHT2,
        GL_QUADRATIC_ATTENUATION,
        0.003
    )