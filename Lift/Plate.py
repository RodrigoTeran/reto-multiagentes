from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np


class Plate:
    def __init__(self):
        self.bottom_plate = [
            # Right face
            [-0.5, 0, 0],
            [-0.5, 0.15, 0],
            [-0.5, 0.15, 1],
            [-0.5, 0, 1],
            # Left face
            [0.5, 0, 0],
            [0.5, 0.15, 0],
            [0.5, 0.15, 1],
            [0.5, 0, 1],
            # Bottom Face
            [-0.5, 0, 0],
            [0.5, 0, 0],
            [0.5, 0, 1],
            [-0.5, 0, 1],
            # Top Face
            [-0.5, 0.15, 0],
            [0.5, 0.15, 0],
            [0.5, 0.15, 1],
            [-0.5, 0.15, 1],
        ]
        self.vertical_plate = [
            [-0.5, 0, 0],
            [-0.5, 1, 0],
            [0.5, 1, 0],
            [0.5, 0, 0],
            [-0.5, 0, 0],
            [-0.5, 1, 0],
            [-0.5, 1, 0.15],
            [-0.5, 0, 0.15],
            [0.5, 0, 0],
            [0.5, 1, 0],
            [0.5, 1, 0.15],
            [0.5, 0, 0.15],
            [-0.5, 0, 0.15],
            [-0.5, 1, 0.15],
            [0.5, 1, 0.15],
            [0.5, 0, 0.15],
        ]

    def render(self):
        glPushMatrix()
        glColor3f(0.7, 0.7, 0.7)
        glBegin(GL_QUADS)
        for point in self.bottom_plate:
            glVertex3fv(point)
        for point in self.vertical_plate:
            glVertex3fv(point)
        glEnd()
        glPopMatrix()
