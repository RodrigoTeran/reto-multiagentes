from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


def Axis():
    glShadeModel(GL_FLAT)
    glBegin(GL_LINES)

    # X axis in red
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-500, 0.0, 0.0)
    glVertex3f(500, 0.0, 0.0)

    # Y axis in green
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, 500, 0.0)
    glVertex3f(0.0, -500, 0.0)

    # Z axis in blue
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, 500)
    glVertex3f(0.0, 0.0, -500)

    glEnd()
    glLineWidth(3)


def draw_cuboid(points: list[list[float]]):
    squares = [
        (0, 1, 2, 3),
        (0, 4, 5, 1),
        (3, 2, 6, 7),
        (4, 7, 6, 5),
        (0, 4, 7, 3),
        (1, 5, 6, 2),
    ]

    for square in squares:
        for i in square:
            glVertex3fv(points[i])


def plane(width: float, length: float, height: float, color: list[float]):
    points = [
        [-width, height, -length],
        [-width, height, length],
        [width, height, length],
        [width, height, -length],
    ]

    glPushMatrix()
    glColor3fv(color)
    glBegin(GL_QUADS)
    for point in points:
        glVertex3fv(point)
    glEnd()
    glPopMatrix()
