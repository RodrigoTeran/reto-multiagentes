from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np
import math

from random import random

TOLERANCE = 1

class Car:
    cars: list["Car"] = []

    def __init__(self, street: int, destination: int):
        self.roof_color = [0.7, 0.8, 1.0]
        self.body_color = [0.7, 0.9, 0.8] 
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
            [0.5, 1.01, 0.5],
            [-0.5, 1.01, 0.5],
            [-0.5, 1.01, -0.5],
            [0.5, 1.01, -0.5],
        ]
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
        if street == 1:
            starting_position = [-1.5, 0, -17.5]
            target_position_to_wait = [-1.5, 0, -7]
        elif street == 2:
            starting_position = [-17.5, 0, 1.5]
            target_position_to_wait = [-7, 0, 1.5]
        elif street == 3:
            starting_position = [1.5, 0, 17.5]
            target_position_to_wait = [1.5, 0, 7]
        elif street == 4:
            starting_position = [17.5, 0, -1.5]
            target_position_to_wait = [7, 0, -1.5]

        if destination == 1:
            target_position_to_turn = [1.5, 0, -7]
            target_position_to_leave = [1.5, 0, -17.5]
        elif destination == 2:
            target_position_to_turn = [-7, 0, -1.5]
            target_position_to_leave = [-17.5, 0, -1.5]
        elif destination == 3:
            target_position_to_turn = [-1.5, 0, 7]
            target_position_to_leave = [-1.5, 0, 17.5]
        elif destination == 4:
            target_position_to_turn = [7, 0, 1.5]
            target_position_to_leave = [17.5, 0, 1.5]

        self.street = street
        self.destination = destination

        self.position = np.array(starting_position, float)
        self.target_position = np.array(starting_position, float) # Current
        
        self.target_position_to_wait = target_position_to_wait
        self.target_position_to_turn = target_position_to_turn
        self.target_position_to_leave = target_position_to_leave

        self.speed = 1
        self.radio = 1.5
        Car.cars.append(self)
        self.id = random()
        
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

        # Render main body
        glColor3f(*self.body_color)
        glBegin(GL_QUADS)
        self.draw_cuboid(self.points)
        glEnd()

        # Render pilot seat
        glColor3f(0.3, 0.3, 0.3)
        glBegin(GL_QUADS)
        for column in self.columns:
            for point in column:
                glVertex3fv(point)
        glEnd()

        # Render roof
        glColor3f(*self.roof_color)
        glBegin(GL_QUADS)
        for point in self.roof_points:
            glVertex3f(*point)
        glEnd()

        glPopMatrix()
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
            

    def update(self):
        if self.step == 0:
            self.go_to_point(self.target_position_to_wait)
        elif self.step == 1:
            self.go_to_point(self.target_position_to_turn)
        elif self.step == 2:
            self.go_to_point(self.target_position_to_leave)

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
                self.step += 1
