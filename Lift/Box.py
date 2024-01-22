from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from Utils import draw_cuboid


class Box:
    boxes: list["Box"] = []

    def __init__(self, position: list[float]):
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
        Box.boxes.append(self)

    def render(self):
        glPushMatrix()
        glTranslate(*self.position)
        glBegin(GL_QUADS)
        draw_cuboid(self.points)
        glEnd()
        glPopMatrix()
