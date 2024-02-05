from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np
import math

from random import random

TOLERANCE = 1

class Car:
    cars: list["Car"] = []

    def __init__(self, street: int, destination: int, texture_car, texture_glass):
        self.texture_car = texture_car
        self.texture_glass = texture_glass
        self.crossed = False
        self.points = [
            [-0.5, 0, 0.5],
            [-0.5, 0.5, 0.5],
            [0.5, 0.5, 0.5],
            [0.5, 0, 0.5],
            [-0.5, 0, -1.5],
            [-0.5, 0.5, -1.5],
            [0.5, 0.5, -1.5],
            [0.5, 0, -1.5],
        ]
        self.roof_points = [
            [0.5, 1.01, -0.3],
            [-0.5, 1.01, -0.3],
            [-0.5, 1.01, -1],
            [0.5, 1.01, -1],
        ]
        self.left_directional = [
            [0.5, 0.6, 0.35],
            [0.25, 0.6, 0.35],
            [0.25, 0.6, 0.5],
            [0.5, 0.6, 0.5]
        ]
        self.right_directional = [
            [-0.5, 0.6, 0.35],
            [-0.25, 0.6, 0.35],
            [-0.25, 0.6, 0.5],
            [-0.5, 0.6, 0.5]
        ]
        self.windows = [
            [  # Ventana delantera
                # base
                [0.5, 0.5, 0.1],
                [-0.5, 0.5, 0.1],
                [-0.5, 0.5, -0.1],
                [0.5, 0.5, -0.1],
                # top
                [0.5, 1.0, -0.25],
                [-0.5, 1.0, -0.25],
                [-0.5, 1.0, -0.45],
                [0.5, 1.0, -0.45],
                # z face
                [0.5, 0.5, 0.1],
                [-0.5, 0.5, 0.1],
                [-0.5, 1.0, -0.25],
                [0.5, 1.0, -0.25],
                # -z face
                [-0.5, 0.5, -0.1],
                [0.5, 0.5, -0.1],
                [0.5, 1.0, -0.45],
                [-0.5, 1.0, -0.45],
                # x face
                [0.5, 0.5, -0.1],
                [0.5, 0.5, 0.1],
                [0.5, 1.0, -0.25],
                [0.5, 1.0, -0.45],
                # -x face
                [-0.5, 0.5, 0.1],
                [-0.5, 0.5, -0.1],
                [-0.5, 1.0, -0.45],
                [-0.5, 1.0, -0.25],
            ],
            [  # Ventana trasera
                # base
                [0.5, 0.5, 0.1 - 1.2],
                [-0.5, 0.5, 0.1 - 1.2],
                [-0.5, 0.5, -0.1 - 1.2],
                [0.5, 0.5, -0.1 - 1.2],
                # top
                [0.5, 1.0, -0.25 - 0.5],
                [-0.5, 1.0, -0.25 - 0.5],
                [-0.5, 1.0, -0.45 - 0.5],
                [0.5, 1.0, -0.45 - 0.5],
                # z face
                [0.5, 0.5, 0.1 - 1.2],
                [-0.5, 0.5, 0.1 - 1.2],
                [-0.5, 1.0, -0.25 - 0.5],
                [0.5, 1.0, -0.25 - 0.5],
                # -z face
                [-0.5, 0.5, -0.1 - 1.2],
                [0.5, 0.5, -0.1 - 1.2],
                [0.5, 1.0, -0.45 - 0.5],
                [-0.5, 1.0, -0.45 - 0.5],
                # x face
                [0.5, 0.5, -0.1 - 1.2],
                [0.5, 0.5, 0.1 - 1.2],
                [0.5, 1.0, -0.25 - 0.5],
                [0.5, 1.0, -0.45 - 0.5],
                # -x face
                [-0.5, 0.5, 0.1 - 1.2],
                [-0.5, 0.5, -0.1 - 1.2],
                [-0.5, 1.0, -0.45 - 0.5],
                [-0.5, 1.0, -0.25 - 0.5]
            ]
        ]

        self.place_car(street, destination)

        self.speed = 1
        self.radio = 1.45
        self.directionals_ticks = 0
        self.max_directionals_ticks = 10
        Car.cars.append(self)
        self.id = random()
        self.is_waiting_for_light = False
    
    def place_car(self, street, destination):
        if street == destination:
            raise Exception("Están prohibidas las vueltas en U... :(")

        if street == 1:
            starting_position = [-1.5, 0, -17.5]
            target_position_to_wait = [-1.5, 0, -8]
        elif street == 2:
            starting_position = [-17.5, 0, 1.5]
            target_position_to_wait = [-8, 0, 1.5]
        elif street == 3:
            starting_position = [1.5, 0, 17.5]
            target_position_to_wait = [1.5, 0, 8]
        elif street == 4:
            starting_position = [17.5, 0, -1.5]
            target_position_to_wait = [8, 0, -1.5]

        tolerance_left_turn = 1.1

        if destination == 1:
            target_position_to_turn = [1.5, 0, -7]
            target_position_to_leave = [1.5, 0, -17.5]
            self.mid_target_position_to_turn = [-tolerance_left_turn, 0, -tolerance_left_turn]
        elif destination == 2:
            target_position_to_turn = [-7, 0, -1.5]
            target_position_to_leave = [-17.5, 0, -1.5]
            self.mid_target_position_to_turn = [-tolerance_left_turn, 0, tolerance_left_turn]
        elif destination == 3:
            target_position_to_turn = [-1.5, 0, 7]
            target_position_to_leave = [-1.5, 0, 17.5]
            self.mid_target_position_to_turn = [tolerance_left_turn, 0, tolerance_left_turn]
        elif destination == 4:
            target_position_to_turn = [7, 0, 1.5]
            target_position_to_leave = [17.5, 0, 1.5]
            self.mid_target_position_to_turn = [tolerance_left_turn, 0, -tolerance_left_turn]

        self.street = street
        self.destination = destination

        self.intent = "straight"

        if self.street <= 3 and self.street == self.destination - 1:
            self.intent = "right"
        if self.street >= 2 and self.street == self.destination + 1:
            self.intent = "left"
        if self.street == 4 and self.destination == 1:
            self.intent = "right"
        if self.street == 1 and self.destination == 4:
            self.intent = "left"

        self.position = np.array(starting_position, float)
        self.target_position = np.array(starting_position, float) # Current
        self.target_position_to_wait = target_position_to_wait
        self.target_position_to_turn = target_position_to_turn
        self.target_position_to_leave = target_position_to_leave

        # dir vectors
        self.dir_vector = [0, 0, 0]
        self.dir_target = self.dir_vector.copy()

        self.moving_to_target = False
        self.step = 0 # 0 -> moverse a la linea, 1 -> dar vuelta, 2 -> irse

    def vector_angle(self, vu, vv):  # calcula el +/-angulo entre 2 vectores
        vvx = vv[2]
        vvy = vv[0]
        vux = vu[2]
        vuy = vu[0]
        return np.degrees(np.arctan2(vvy, vvx) - np.arctan2(vuy, vux))
    
    def rotate_dir_vector(self):  # rota progresivamente el vector de dir hasta alcanzar la dir objetivo
        if not np.array_equal(self.dir_vector, self.dir_target):
            dif = self.vector_angle(self.dir_vector, self.dir_target)
            if (
                abs(dif) < 2
            ):  # si el abs del angulo de dif es menor a 2(la rotacion por iteracion) se termina de rotar igualando la dir al target
                self.dir_vector = self.dir_target
            elif dif < 0:
                degree = np.radians(2)
                x = self.dir_vector[0]
                y = self.dir_vector[2]
                self.dir_vector[0] = (x * np.cos(degree)) - (y * np.sin(degree))
                self.dir_vector[2] = (x * np.sin(degree)) + (y * np.cos(degree))
            elif dif > 0:
                degree = np.radians(2)
                x = self.dir_vector[0]
                y = self.dir_vector[2]
                self.dir_vector[0] = (x * np.cos(degree)) + (y * np.sin(degree))
                self.dir_vector[2] = -(x * np.sin(degree)) + (y * np.cos(degree))
        else:
            self.dir_vector = self.dir_vector

    def go_to_point(self, target):
        self.target_position = np.array(target)
        direction = self.target_position - self.position
        self.dir_target = direction / np.linalg.norm(direction)
        self.dir_vector = self.dir_target
        self.moving_to_target = True

    def detCol(self):

        for car in Car.cars:
            if car.id == self.id: continue

            # Calcula la distancia entre el lift y el box
            dist = math.sqrt((car.position[0] - self.position[0])**2 + (car.position[2] - self.position[2])**2)

            sum_radios = car.radio + self.radio

            if dist <= sum_radios:
                return car
        
        return None    

    def draw_cuboid(self, points: list[list[float]]):
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
    
    def render(self):
        glPushMatrix()
        glTranslate(*self.position)

        glRotate(
            self.vector_angle([0, 0, 1], self.dir_vector), 0, 1, 0
        )

        # Activar y enlazar la textura
        glPushMatrix()
        glColor3fv([1, 1, 1])

        # Render main body
        if self.street == 1:
            colorBody = [1.0, 0.0, 0.0]
        elif self.street == 2:
            colorBody = [227.0/255, 45.0/255, 243.0/255]
        elif self.street == 3:
            colorBody = [222.0/255, 145.0/255, 54.0/255]
        elif self.street == 4:
            colorBody = [171.0/255, 230.0/255, 250.0/255]
        

        glColor3f(*colorBody)
        glBegin(GL_QUADS)
        self.draw_cuboid(self.points)
        glEnd()

        # Render roof
        glColor3f(*colorBody)
        glBegin(GL_QUADS)
        for point in self.roof_points:
            glVertex3f(*point)
        glEnd()

        # Desactivar el uso de texturas
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)

        # Render windows
        glColor3f(*[0.0, 0.0, 1.0])
        glBegin(GL_QUADS)
        for window in self.windows:
            for point in window:
                glVertex3fv(point)
        glEnd()

        # Render directionals        
        off = [0.0, 1.0, 1.0]
        on = [1.0, 1.0, 0.0]

        # left
        if self.intent == "left":
            if self.directionals_ticks < self.max_directionals_ticks / 2:
                glColor3f(*off)
            else:
                glColor3f(*on)
        else:
            glColor3f(*off)

        glBegin(GL_QUADS)
        for point in self.left_directional:
            glVertex3f(*point)
        glEnd()

        # right
        if self.intent == "right":
            if self.directionals_ticks < self.max_directionals_ticks / 2:
                glColor3f(*off)
            else:
                glColor3f(*on)
        else:
            glColor3f(*off)

        glBegin(GL_QUADS)
        for point in self.right_directional:
            glVertex3f(*point)
        glEnd()

        glPopMatrix()

        self.directionals_ticks = (self.directionals_ticks + 1) % self.max_directionals_ticks

        self.update()


    def stop_cars_in_same_lane(self, car: "Car"):
        if self.street == 1:
            # la z debe ser mayor
            if car.position[2] <= self.position[2]:
                return car
            return self
        
        elif self.street == 2:
            # la x debe ser mayor
            if car.position[0] <= self.position[0]:
                return car
            return self
        
        elif self.street == 3:
            # la z debe ser menor
            if car.position[2] >= self.position[2]:
                return car
            return self
        
        elif self.street == 4:
            # la x debe ser menor
            if car.position[0] >= self.position[0]:
                return car
            return self
        
    def green_light(self):
        self.is_waiting_for_light = False
    
    def red_light(self):
        self.is_waiting_for_light = True

    def update(self):
        if self.step == 0:
            self.go_to_point(self.target_position_to_wait)
        elif self.step == 1 or self.step == 1.5:
            if self.intent == "left":
                if self.step == 1:
                    self.go_to_point(self.mid_target_position_to_turn) # go to center
                else:
                    self.go_to_point(self.target_position_to_turn)
            else:
                self.go_to_point(self.target_position_to_turn)
        elif self.step == 2:
            self.go_to_point(self.target_position_to_leave)
        elif self.step == 3:
            # volver al inicio
            self.crossed = True
            self.step = 0
            self.place_car(self.street, self.destination)

        car = self.detCol()
        if car is not None:
            if car.street != self.street:
                # Both
                self.moving_to_target = False
                car.moving_to_target = False
                return
            
            # same street
            # quitar movimiento solo al que va más atrás
            annoying_car = self.stop_cars_in_same_lane(car)
            annoying_car.moving_to_target = False
        
        if self.moving_to_target:
            diff = np.linalg.norm(self.target_position - self.position)
            if diff > TOLERANCE:
                self.position += np.array(self.dir_vector, float) * self.speed
            else:
                # ya ha llegado a ese destino
                if self.is_waiting_for_light and self.step == 0: return
                
                if self.intent == "left" and self.step == 1:
                    self.step = 1.5
                else:
                    self.step = math.floor(self.step + 1)            
        pass
