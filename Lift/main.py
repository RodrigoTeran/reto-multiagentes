import pygame
import math
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from random import randint

from Lift import Lift
from Utils import Axis, plane
from Box import Box
from Warehouse import Warehouse

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

FOVY = 30.0
ZNEAR = 1.0
ZFAR = 500.0

EYE_X = 50.0
EYE_Y = 50.0
EYE_Z = 50.0
CENTER_X = 0
CENTER_Y = 0
CENTER_Z = 0
UP_X = 0
UP_Y = 1
UP_Z = 0

BOX_COLOR = [0.45, 0.35, 0.23]

PLANE_WIDTH = 20
PLANE_LENGTH = 20


def Init():
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: Lift")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, SCREEN_WIDTH / SCREEN_HEIGHT, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

def main():
    lifts = []
    for _ in range(5):
        lifts.append(Lift([1.0, 0, 2], [0, 0, 0], 0.1))
    boxes = []
    for _ in range(15):
        boxes.append(
            Box(
                [
                    randint(-PLANE_WIDTH, PLANE_WIDTH),
                    1,
                    randint(-PLANE_LENGTH, PLANE_LENGTH),
                ],
                BOX_COLOR,
            )
        )
    warehouse = Warehouse([0, 0, 0], 2)

    Init()
    done = False
    while not done:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    done = True
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_ESCAPE:
                            done = True

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        Axis()
        plane(PLANE_WIDTH, PLANE_LENGTH, 0, [1, 1, 1])
        for lift in lifts:
            lift.render()
        for box in boxes:
            box.render()
        warehouse.render()

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()


if __name__ == "__main__":
    main()
