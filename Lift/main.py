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

BOX_COLOR = [0.45, 0.35, 0.23]


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


def liftHitBox(lift: Lift, box: Box):
    """Funcion que checa si el hitbox del lift y el hitbox de la caja se intersectan,
    mediante el calculo de distancias eucleidianas de los centros de las hitboxes.

    Si la suma de los radios de las hitboxes es menor a la distancia entre los centros de las hitboxes,
    entonces se intersectan.

        - Box hitbox: Se considera el radio de la caja como la distancia de su centro a uno de sus vertices
        - Lift hitbox: Se considera a la bottom plate como la hitbox del lift, por lo que su radio es la distancia
            de su centro a uno de sus vertices.

    Esta funcion se debe llamar por cada combinacion de lift y caja, para determinar si se intersectan o no.
    """

    box_center = box.position

    if (lift.hitbox_radius + box.radius) < (
        (lift.hitbox_center[0] - box_center[0]) ** 2
        + (lift.hitbox_center[1] - box_center[1]) ** 2
        + (lift.hitbox_center[2] - box_center[2]) ** 2
    ) ** 0.5:
        print(f"El lift {lift} y la caja {box} se intersectan")
    else:
        print("Falso")

    # TODO: Implementar la funcion de carga, traslado y descarga de cajas


def main():
    lift = Lift([0, 0, 0], 2)
    boxes = []
    boxes.append(Box([4, 1, 2], BOX_COLOR))
    boxes.append(Box([-2, 1, -2], BOX_COLOR))

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
        if keys[pygame.K_w]:
            lift.go_to_point([0, 0, 1])

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
