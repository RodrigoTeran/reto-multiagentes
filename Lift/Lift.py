from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np

from Plate import Plate
from Utils import draw_cuboid

import random


class Lift:
    def __init__(self, position: list[float], angular_speed: float):
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
        # self.direction = direction
        # self.target_direction = -90
        self.angular_speed = angular_speed
        self.plate = Plate(self.plate_color)
        
        self.dir_vector = [0,0,0]   #dir actual
        self.dir_vector[0] = random.randint(1,100) / 100 * (-1 + (random.randint(0,1) * 2))     #numero de +-0.01 a +-1.00
        self.dir_vector[2] = np.sqrt(1-(self.dir_vector[0]*self.dir_vector[0]))* (-1 + (random.randint(0,1) * 2))   #+/-z para ser unitario con [0]
        
        self.dir_target = self.dir_vector   #dir objetivo
        
        
        # Se considera la hitbox como la bottom plate del lift 
        self.hitbox_center = self.plate.bottom_plate_center
        self.hitbox_radius = self.plate.bottom_plate_radius  # El radio del hitbox siempre es el mismo, ya que la bottom plate no cambia de tamaño
    
    def vector_angle(self, vu, vv):     #calcula el +/-angulo entre 2 vectores
        vvx = vv[2]
        vvy = vv[0]
        vux = vu[2]
        vuy = vu[0]
        return(np.degrees(np.arctan2(vvy,vvx) - np.arctan2(vuy,vux)))
    
    def rotate_dir_vector(self):    #rota progresivamente el vector de dir hasta alcanzar la dir objetivo
        
        if self.dir_vector != self.dir_target:
            dif = self.vector_angle(self.dir_vector, self.dir_target)
            print(dif)
            if abs(dif) < 0.5:      #si el abs del angulo de dif es menor a 0.5(la rotacion por iteracion) se termina de rotar igualando la dir al target
                self.dir_vector = self.dir_target
            elif dif < 0:
                degree = np.radians(0.5)
                x = self.dir_vector[0]
                y = self.dir_vector[2]
                self.dir_vector[0] = (x * np.cos(degree)) - (y * np.sin(degree))
                self.dir_vector[2] = (x * np.sin(degree)) + (y * np.cos(degree))
            elif dif > 0:
                degree = np.radians(0.5)
                x = self.dir_vector[0]
                y = self.dir_vector[2]
                self.dir_vector[0] = (x * np.cos(degree)) + (y * np.sin(degree))
                self.dir_vector[2] = - (x * np.sin(degree)) + (y * np.cos(degree))
        else:
            self.dir_vector = self.dir_vector
    
    def render(self):
        glPushMatrix()
        glTranslate(*self.position)
        
        # self.rotate_dir_vector()
        glRotate(self.vector_angle([0,0,1], self.dir_vector), 0,1,0)    #rota con angulo respecto a eje z ya que el frente del montacargas esta dibujado en eje z

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
        if self.dir_vector != self.dir_target:
            self.rotate_dir_vector()

            
        # TODO: En la funcion update, calcular las coordenadas del nuevo centro de la hitbox y actualizar el atributo self.hitbox_center
        # TODO: Esto se hace una vez que se haya implementado el movimiento de los lifts (Movimiento del robot #5)