import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from Utils import plane, horizons, solid_plane

import sys

sys.path.append("..")

from TrafficLight import TrafficLight
from Car import Car
from objloader import OBJ
import simulation

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
textures = []

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


def Texturas(filepath):
    textures.append(glGenTextures(1))
    id = len(textures) - 1
    glBindTexture(GL_TEXTURE_2D, textures[id])
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    image = pygame.image.load(filepath).convert()
    w, h = image.get_rect().size
    image_data = pygame.image.tostring(image, "RGBA")
    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data
    )
    glGenerateMipmap(GL_TEXTURE_2D)
    glDisable(GL_TEXTURE_2D)


traffic_lights = []  # facing north, east, south, west
cars = []
positions = [[0, 5, -10], [-10, 5, 0], [0, 5, 10], [10, 5, 0]]
rotations = [[0, 0, 0, 0], [90, 0, 1, 0], [180, 0, 1, 0], [-90, 0, 1, 0]]

for i in range(4):
    traffic_lights.append(TrafficLight(positions[i], rotations[i]))


def add_cars(cars_to_add):  # cars_to_add: [(from, to), (from, to)]
    for new_car in cars_to_add:
        cars.append(Car(new_car[0], new_car[1], textures[2], textures[3]))


# Example of how events look like:
# events = [
#     # Event 1
#     {
#         'cars_to_add': [(4, 2), (1, 2), (1, 3), (1, 4), (4, 3), (3, 2), (3, 2), (3, 2), (4, 2), (4, 2), (4, 2)],
#         'traffice_light_colors': ['green', 'red', 'red', 'red'] # Each index represents a traffic light
#     },
#     # Event 2
#     {
#         'traffice_light_colors': ['red', 'green', 'red', 'red']
#     },
# ]

# Which traffic light is in front of which street
STREET_TO_TRAFFIC_LIGHT = {1: 2, 2: 3, 3: 0, 4: 1}


def main(events):
    Init()
    Texturas("reto/assets/Suelo.bmp")
    Texturas("reto/assets/cielo.bmp")
    Texturas("reto/assets/carMetalic.bmp")
    Texturas("reto/assets/glass.bmp")
    Texturas("reto/assets/concrete.bmp")

    building = OBJ("reto/assets/Apartment_Building_01_obj.obj")
    building2 = OBJ("reto/assets/building.obj")
    tree = OBJ("reto/assets/masktree3.obj")
    tree2 = OBJ("reto/assets/masktree3.obj")
    tree3 = OBJ("reto/assets/masktree3.obj")
    tree4 = OBJ("reto/assets/masktree3.obj")
    tree5 = OBJ("reto/assets/masktree3.obj")
    tree6 = OBJ("reto/assets/masktree3.obj")

    # Execute events from simultion
    for event_dict in events:
        # Check if new cars are added in event
        if "cars_to_add" in event_dict:
            add_cars(event_dict["cars_to_add"])

        if "traffice_light_colors" not in event_dict:
            continue
        event_done = False
        while not event_done:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        event_done = True
                        pygame.quit()
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_ESCAPE:
                                event_done = True

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            plane(PLANE_WIDTH, PLANE_LENGTH, 0, [1, 1, 1], textures[0])
            horizons(
                PLANE_WIDTH,
                PLANE_LENGTH,
                25,
                [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0]],
                textures[1],
            )
            solid_plane(
                200,
                200,
                -2,
                [
                    0 / 255,
                    150 / 255,
                    64 / 255,
                ],
            )
            solid_plane(
                100,
                2.5,
                -0.01,
                [
                    84 / 255,
                    83 / 255,
                    83 / 255,
                ],
            )
            solid_plane(
                2.5,
                100,
                -0.01,
                [
                    84 / 255,
                    83 / 255,
                    83 / 255,
                ],
            )
            solid_plane(
                4.75,
                100,
                -0.11,
                [
                    179 / 255,
                    178 / 255,
                    178 / 255,
                ],
            )
            solid_plane(
                100,
                4.75,
                -0.11,
                [
                    179 / 255,
                    178 / 255,
                    178 / 255,
                ],
            )

            # Draw traffic lights with there color
            for i in range(4):
                traffic_lights[i].draw(event_dict["traffice_light_colors"][i])

            is_rem_cars = False
            # Check if all cars that should have crossed have crossed.
            for car in cars:
                trafic_light_index = STREET_TO_TRAFFIC_LIGHT[car.street]
                if (
                    not car.crossed
                    and event_dict["traffice_light_colors"][trafic_light_index]
                    == "green"
                ):
                    car.green_light()
                    is_rem_cars = True
                else:
                    car.red_light()

                if not car.crossed:
                    car.render()

            if not is_rem_cars:
                event_done = True
            glBindTexture(GL_TEXTURE_2D, 5)
            glPushMatrix()
            glColor3f(1, 1, 1)
            glTranslate(14, 0, -10)
            glScale(0.01, 0.01, 0.01)
            building.render()
            glPopMatrix()
            glPushMatrix()
            glTranslate(-12, 0, -12)
            glScale(0.2, 0.2, 0.2)
            building2.render()
            glPopMatrix()
            glPushMatrix()
            glTranslate(-10, 0, 10)
            glScale(0.8, 0.8, 0.8)
            glRotate(-30, 0, 1, 0)
            tree.render()
            glTranslate(-2, 0, 5)
            tree2.render()
            glTranslate(5, 0, 3)
            tree3.render()
            glPopMatrix()
            glPushMatrix()
            glTranslate(10, 0, 10)
            glScale(0.5, 0.5, 0.5)
            tree4.render()
            glTranslate(2, 0, 3)
            tree5.render()
            glTranslate(-5, 0, -2)
            tree6.render()
            glPopMatrix()

            pygame.display.flip()
            pygame.time.wait(1)

    pygame.quit()


if __name__ == "__main__":
    events = simulation.runModel()
    main(events)
