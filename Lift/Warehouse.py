from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from Utils import draw_cuboid


class Warehouse:
    def __init__(self, position: list[float], scale: float):
        self.points = [
            [-0.5, -0.5, 0.5],
            [-0.5, 0.5, 0.5],
            [0.5, 0.5, 0.5],
            [0.5, -0.5, 0.5],
            [-0.5, -0.5, -0.5],
            [-0.5, 0.5, -0.5],
            [0.5, 0.5, -0.5],
            [0.5, -0.5, -0.5],
        ]
        self.position = position
        self.scale = scale
        self.color = [0.21, 0.14, 0.7]

    def render(self):
        glPushMatrix()
        glTranslate(*self.position)
        glScale(self.scale, self.scale, self.scale)
        glColor3fv(self.color)
        glBegin(GL_QUADS)
        draw_cuboid(self.points)
        glEnd()
        glPopMatrix()
