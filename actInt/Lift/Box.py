from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math
from Utils import draw_cuboid


class Box:
    boxes: list["Box"] = []

    def __init__(self, position: list[float], color: list[float]):
        self.points = [
            [-0.5, -0.5, 0.5],
            [-0.5, 0.5, 0.5],
            [0.5, 0.5, 0.5],
            [0.5, -0.5, 0.5],
            [-0.5, -0.5, -0.5],
            [-0.5, 0.5, -0.5],
            [0.5, 0.5, -0.5],
            [0.5, -0.5, -0.5],
        ]
        
        self.scale = 1.0
        self.radio = math.sqrt(self.scale*self.scale + self.scale*self.scale)
        self.position = position
        self.delivered = False
        self.color = color
        Box.boxes.append(self)
        # El centro del cubo son las coordenadas de self.position, por eso no creamos un atributo self.center
        # Como los cubos son inmobiles, los centros no se actualizan
        self.radius = 0.866  #((0.5 - self.center[0]) ** 2 + (0.5 - self.center[1]) ** 2 + (0.5 - self.center[2]) ** 2) ** 0.5 


    def render(self):
        glPushMatrix()
        glTranslate(*self.position)
        glColor(*self.color)
        
        glBegin(GL_QUADS)
        draw_cuboid(self.points)
        glEnd()
        glPopMatrix()
