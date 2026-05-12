from OpenGL.GL import *
from OpenGL.GLU import *
import math


# ─────────────────────────────────────────────
#  KAMERA
# ─────────────────────────────────────────────
class Camera:
    def __init__(self):
        self.reset()

    def reset(self):
        self.dist = 38.0
        self.yaw = 30.0
        self.pitch = 22.0
        self.tx, self.ty, self.tz = 0.0, 5.0, 0.0

    def apply(self):
        glLoadIdentity()
        yr = math.radians(self.yaw)
        pr = math.radians(self.pitch)
        ex = self.tx + self.dist * math.cos(pr) * math.sin(yr)
        ey = self.ty + self.dist * math.sin(pr)
        ez = self.tz + self.dist * math.cos(pr) * math.cos(yr)
        gluLookAt(ex, ey, ez, self.tx, self.ty, self.tz, 0, 1, 0)

    def rotate(self, dy, dp):
        self.yaw += dy
        self.pitch = max(-80, min(80, self.pitch + dp))

    def zoom(self, d):
        self.dist = max(6, min(90, self.dist - d * 2.5))

    def move(self, dx, dy, dz):
        self.tx += dx
        self.ty += dy
        self.tz += dz

    def move_relative(self, forward=0, right=0, up=0):

        yr = math.radians(self.yaw)

        fx = math.sin(yr)
        fz = math.cos(yr)

        rx = math.cos(yr)
        rz = -math.sin(yr)

        self.tx += fx * forward + rx * right
        self.tz += fz * forward + rz * right
        self.ty += up
