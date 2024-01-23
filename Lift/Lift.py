from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np

from Plate import Plate
from Utils import draw_cuboid


class Lift:
    def __init__(self, position: list[float], direction: float, angular_speed: float):
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
            [0.5, 1.01, -0.5]
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
        self.position = np.array(position)
        self.direction = direction
        self.target_direction = -90
        self.angular_speed = angular_speed
        self.plate = Plate(self.plate_color)
        
        # Se considera la hitbox como la bottom plate del lift 
        self.hitbox_center = self.plate.bottom_plate_center
        self.hitbox_radius = self.plate.bottom_plate_radius  # El radio del hitbox siempre es el mismo, ya que la bottom plate no cambia de tamaño
        

    def render(self):
        glPushMatrix()
        glTranslate(*self.position)
        glRotate(self.direction, 0, 1, 0)

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

    def update(self):
        if self.target_direction < self.direction:
            self.direction -= 1 * self.angular_speed

        if self.target_direction > self.direction:
            self.direction += 1 * self.angular_speed
            
        # TODO: En la funcion update, calcular las coordenadas del nuevo centro de la hitbox y actualizar el atributo self.hitbox_center
        # TODO: Esto se hace una vez que se haya implementado el movimiento de los lifts (Movimiento del robot #5)