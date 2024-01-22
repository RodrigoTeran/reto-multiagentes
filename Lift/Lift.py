from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np


class Lift:
    def __init__(self, position: list[float], direction: float, angular_speed: float):
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
        self.columns = [
            [  # poste A
                # base
                [0.5, 0.5, 0.5],
                [0.3, 0.5, 0.5],
                [0.3, 0.5, 0.3],
                [0.5, 0.5, 0.3],
                # top
                [0.5, 1.0, 0.5],
                [0.3, 1.0, 0.5],
                [0.3, 1.0, 0.3],
                [0.5, 1.0, 0.3],
                # z face
                [0.5, 0.5, 0.5],
                [0.3, 0.5, 0.5],
                [0.3, 1.0, 0.5],
                [0.5, 1.0, 0.5],
                # -z face
                [0.3, 0.5, 0.3],
                [0.5, 0.5, 0.3],
                [0.5, 1.0, 0.3],
                [0.3, 1.0, 0.3],
                # x face
                [0.5, 0.5, 0.3],
                [0.5, 0.5, 0.5],
                [0.5, 1.0, 0.5],
                [0.5, 1.0, 0.3],
                # -x face
                [0.3, 0.5, 0.5],
                [0.3, 0.5, 0.3],
                [0.3, 1.0, 0.3],
                [0.3, 1.0, 0.5],
            ],
            [  # poste B
                # base
                [-0.5, 0.5, 0.5],
                [-0.5, 0.5, 0.3],
                [-0.3, 0.5, 0.3],
                [-0.3, 0.5, 0.5],
                # top
                [-0.5, 1.0, 0.5],
                [-0.5, 1.0, 0.3],
                [-0.3, 1.0, 0.3],
                [-0.3, 1.0, 0.5],
                # z face
                [-0.3, 0.5, 0.5],
                [-0.5, 0.5, 0.5],
                [-0.5, 1.0, 0.5],
                [-0.3, 1.0, 0.5],
                # -z face
                [-0.5, 0.5, 0.3],
                [-0.3, 0.5, 0.3],
                [-0.3, 1.0, 0.3],
                [-0.5, 1.0, 0.3],
                # x face
                [-0.3, 0.5, 0.3],
                [-0.3, 0.5, 0.5],
                [-0.3, 1.0, 0.5],
                [-0.3, 1.0, 0.3],
                # -x face
                [-0.5, 0.5, 0.5],
                [-0.5, 0.5, 0.3],
                [-0.5, 1.0, 0.3],
                [-0.5, 1.0, 0.5],
            ],
            [  # poste C
                # base
                [-0.5, 0.5, -0.3],
                [-0.5, 0.5, -0.5],
                [-0.3, 0.5, -0.5],
                [-0.3, 0.5, -0.3],
                # top
                [-0.5, 1.0, -0.3],
                [-0.5, 1.0, -0.5],
                [-0.3, 1.0, -0.5],
                [-0.3, 1.0, -0.3],
                # z face
                [-0.3, 0.5, -0.3],
                [-0.5, 0.5, -0.3],
                [-0.5, 1.0, -0.3],
                [-0.3, 1.0, -0.3],
                # -z face
                [-0.5, 0.5, -0.5],
                [-0.3, 0.5, -0.5],
                [-0.3, 1.0, -0.5],
                [-0.5, 1.0, -0.5],
                # x face
                [-0.3, 0.5, -0.5],
                [-0.3, 0.5, -0.3],
                [-0.3, 1.0, -0.3],
                [-0.3, 1.0, -0.5],
                # -x face
                [-0.5, 0.5, -0.3],
                [-0.5, 0.5, -0.5],
                [-0.5, 1.0, -0.5],
                [-0.5, 1.0, -0.3],
            ],
            [  # poste D
                # base
                [0.3, 0.5, -0.3],
                [0.3, 0.5, -0.5],
                [0.5, 0.5, -0.5],
                [0.5, 0.5, -0.3],
                # top
                [0.3, 1.0, -0.3],
                [0.3, 1.0, -0.5],
                [0.5, 1.0, -0.5],
                [0.5, 1.0, -0.3],
                # z face
                [0.5, 0.5, -0.3],
                [0.3, 0.5, -0.3],
                [0.3, 1.0, -0.3],
                [0.5, 1.0, -0.3],
                # -z face
                [0.3, 0.5, -0.5],
                [0.5, 0.5, -0.5],
                [0.5, 1.0, -0.5],
                [0.3, 1.0, -0.5],
                # x face
                [0.5, 0.5, -0.5],
                [0.5, 0.5, -0.3],
                [0.5, 1.0, -0.3],
                [0.5, 1.0, -0.5],
                # -x face
                [0.3, 0.5, -0.3],
                [0.3, 0.5, -0.5],
                [0.3, 1.0, -0.5],
                [0.3, 1.0, -0.3],
            ],
        ]
        self.position = np.array(position)
        self.direction = direction
        self.new_direction = 180
        self.angular_speed = angular_speed

    def render(self):
        glPushMatrix()
        glTranslate(*self.position)
        glRotate(self.direction, 0, 1, 0)
        glColor3f(1, 1, 1)
        glBegin(GL_QUADS)
        for point in self.points:
            glVertex3fv(point)
        glEnd()
        glColor3f(0.3, 0.3, 0.3)
        glBegin(GL_QUADS)
        for column in self.columns:
            for point in column:
                glVertex3fv(point)
        glEnd()
        glPopMatrix()
        self.update()

    def set_direction(self, new_direction: float):
        self.new_direction = new_direction

    def update(self):
        if self.new_direction < self.direction:
            self.direction -= 1 * self.angular_speed

        if self.new_direction > self.direction:
            self.direction += 1 * self.angular_speed
