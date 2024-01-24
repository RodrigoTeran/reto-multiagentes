from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np
from Box import Box
from Warehouse import Warehouse
import math

from Plate import Plate
from Utils import draw_cuboid

import random

TOLERANCE = 0.1


class Lift:
    def __init__(self, position: list[float], direction: list[float], speed: float):
        self.roof_color = [0.7, 0.8, 1.0]
        self.body_color = [0.7, 0.9, 0.8]
        self.plate_color = [0.7, 0.7, 0.7]
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
        self.position = np.array(position, float)
        self.target_position = np.array(position, float)
        self.speed = speed
        self.plate = Plate(self.plate_color)
        
        self.scale = 0.2
        self.radio = math.sqrt(self.scale*self.scale + self.scale*self.scale)

        self.dir_vector = [0, 0, 0]  # dir actual
        self.dir_vector[0] = (
            random.randint(1, 100) / 100 * (-1 + (random.randint(0, 1) * 2))
        )  # numero de +-0.01 a +-1.00
        self.dir_vector[2] = np.sqrt(1 - (self.dir_vector[0] * self.dir_vector[0])) * (
            -1 + (random.randint(0, 1) * 2)
        )  # +/-z para ser unitario con [0]

        self.dir_target = self.dir_vector.copy()  # dir objetivo

        # Se considera la hitbox como la bottom plate del lift
        self.hitbox_center = self.plate.bottom_plate_center
        self.hitbox_radius = (
            self.plate.bottom_plate_radius
        )  # El radio del hitbox siempre es el mismo, ya que la bottom plate no cambia de tamaño
        
        self.warehouse = Warehouse([0,0,0], 2)
        self.moving_to_target = False

    def vector_angle(self, vu, vv):  # calcula el +/-angulo entre 2 vectores
        vvx = vv[2]
        vvy = vv[0]
        vux = vu[2]
        vuy = vu[0]
        return np.degrees(np.arctan2(vvy, vvx) - np.arctan2(vuy, vux))

    def rotate_dir_vector(
        self,
    ):  # rota progresivamente el vector de dir hasta alcanzar la dir objetivo
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
        self.moving_to_target = True

    def render(self):
        glPushMatrix()
        glTranslate(*self.position)

        # self.rotate_dir_vector()
        glRotate(
            self.vector_angle([0, 0, 1], self.dir_vector), 0, 1, 0
        )  # rota con angulo respecto a eje z ya que el frente del montacargas esta dibujado en eje z

        # Render main body
        glColor3f(*self.body_color)
        glBegin(GL_QUADS)
        draw_cuboid(self.points)
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

        # Render Plate
        glPushMatrix()
        glTranslate(0, 0, 0.51)
        self.plate.render()
        glPopMatrix()

        glPopMatrix()
        self.update()
        
    def detCol(self):
        for box in Box.boxes:
            # Calcula la distancia entre el lift y el box
            dist = math.sqrt((box.position[0] - self.position[0])**2 + (box.position[2] - self.position[2])**2)

            # Asumiendo que 'radio' es el radio del box y self tiene una propiedad similar
            sum_radios = box.radio + self.radio

            # Si hay colisión, detiene el movimiento del self
            if(dist <= sum_radios):
                # Se detiene el movimiento del self
                return box
                # self.head_to_origin()
        
        return None
    
    def detWarehouseCol(self):
        # Calcula la distancia entre el lift y el warehouse
        dist = math.sqrt((self.warehouse.position[0] - self.position[0])**2 + 
                         (self.warehouse.position[2] - self.position[2])**2)

        # Asumiendo que 'radio' es el radio del warehouse y self tiene una propiedad similar
        sum_radios = self.warehouse.radio + self.radio

        # Si hay colisión, devuelve True
        return dist <= sum_radios
    
    def reset_to_safe_position(self):
        # Establece una nueva posición objetivo dentro de los límites permitidos
        self.target_position = [random.randint(-20, 20), 0, random.randint(-20, 20)]
        # Calcula la nueva dirección
        direction = self.target_position - self.position
        self.dir_target = direction / np.linalg.norm(direction)

    def update(self):
        if not self.moving_to_target:
            box = self.detCol()
            if(box != None and len(self.plate.boxes) == 0):
                self.plate.boxes.append(box)
                self.moving_to_target = True
                # Establece el warehouse como el target
                self.target_position = np.array(self.warehouse.position)
                direction = self.target_position - self.position
                self.dir_vector = direction / np.linalg.norm(direction)
        
        if self.moving_to_target:
            if np.linalg.norm(self.target_position - self.position) > TOLERANCE:
                self.position += np.array(self.dir_vector, float) * self.speed
            
            if self.detWarehouseCol():
                # Entregar la caja y volver al comportamiento normal
                self.plate.boxes.clear()
                self.moving_to_target = False
                self.reset_to_safe_position()
        else:
            if not np.array_equal(self.dir_vector, self.dir_target):
                self.rotate_dir_vector()
                return

            # TODO: En la funcion update, calcular las coordenadas del nuevo centro de la hitbox y actualizar el atributo self.hitbox_center
            # TODO: Esto se hace una vez que se haya implementado el movimiento de los lifts (Movimiento del robot #5)
            # Calculates if distance between target and current is lower than tolerance and moves towards the objective if not.
            if np.linalg.norm(self.target_position - self.position) > TOLERANCE:
                self.position += np.array(self.dir_vector, float) * self.speed
            else:
                self.target_position[0] = random.randint(-20, 20)
                self.target_position[2] = random.randint(-20, 20)
                self.dir_target = [
                    *(
                        (self.target_position - self.position)
                        / np.linalg.norm(self.position - self.target_position)
                    )
                ]
