from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np


class Lift:
    def __init__(self):
        self.points = np.array(
            [
                # Rectángulo perfil 1
                [-0.5, 0, 0.5],
                [-0.5, 0, -1.5],
                [-0.5, 0.5, -1.5],
                [-0.5, 0.5, 0.5],
                # Rectángulo perfil 2
                [0.5, 0, 0.5],
                [0.5, 0.5, 0.5],
                [0.5, 0.5, -1.5],
                [0.5, 0, -1.5],
                # Rectángulo arriba 1
                [-0.5, 0.5, 0.5],
                [-0.5, 0.5, -1.5],
                [0.5, 0.5, -1.5],
                [0.5, 0.5, 0.5],
                # Rectángulo abajo 2
                [-0.5, 0, 0.5],
                [0.5, 0, 0.5],
                [0.5, 0, -1.5],
                [-0.5, 0, -1.5],
                # Rectángulo en frente 1
                [0.5, 0, 0.5],
                [-0.5, 0, 0.5],
                [-0.5, 0.5, 0.5],
                [0.5, 0.5, 0.5],
                # Rectángulo en atrás 2
                [0.5, 0, -1.5],
                [0.5, 0.5, -1.5],
                [-0.5, 0.5, -1.5],
                [-0.5, 0, -1.5],
            ]
        )

    def render(self):
        glColor3f(1, 1, 1)
        glBegin(GL_QUADS)
        for point in self.points:
            glVertex3fv(point)
        glEnd()
