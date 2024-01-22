import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from Lift import Lift
from Utils import Axis
from Box import Box

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

FOVY = 30.0
ZNEAR = 1.0
ZFAR = 500.0

EYE_X = 20.0
EYE_Y = 20.0
EYE_Z = 20.0
CENTER_X = 0
CENTER_Y = 0
CENTER_Z = 0
UP_X = 0
UP_Y = 1
UP_Z = 0


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
    lift = Lift([0, 0, 0], 0, 2)
    boxes = []
    boxes.append(Box([1, 1, 1]))
    boxes.append(Box([-2, 1, -2]))

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

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            lift.target_direction += 1
        if keys[pygame.K_RIGHT]:
            lift.target_direction -= 1
        if keys[pygame.K_UP]:
            lift.plate.target_height += 0.001 * 3
        if keys[pygame.K_DOWN]:
            lift.plate.target_height -= 0.001 * 3

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        Axis()
        lift.render()
        for box in boxes:
            box.render()

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()


if __name__ == "__main__":
    main()
