from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np

from Utils import draw_cuboid


class Plate:
    def __init__(self):
        self.bottom_plate = [
            [-0.5, 0, 1],
            [-0.5, 0.15, 1],
            [0.5, 0.15, 1],
            [0.5, 0, 1],
            [-0.5, 0, 0],
            [-0.5, 0.15, 0],
            [0.5, 0.15, 0],
            [0.5, 0, 0],
        ]
        self.vertical_plate = [
            [-0.5, 0, 0.15],
            [-0.5, 1, 0.15],
            [0.5, 1, 0.15],
            [0.5, 0, 0.15],
            [-0.5, 0, 0],
            [-0.5, 1, 0],
            [0.5, 1, 0],
            [0.5, 0, 0],
        ]
        self.curr_height = 0
        self.target_height = 0
        self.max_height = 0.5
        self.bottom_plate_center = [0, self.curr_height, 0]
        self.bottom_plate_radius = 0.711 #((0.5 - self.bottom_plate_center[0]) ** 2 + (0.15 - self.bottom_plate_center[1]) ** 2 + (1 - self.bottom_plate_center[2]) ** 2) ** 0.5 
    
    def render(self):
        glPushMatrix()
        glColor3f(0.7, 0.7, 0.7)
        glTranslate(0, self.curr_height, 0)
        glBegin(GL_QUADS)
        draw_cuboid(self.bottom_plate)
        draw_cuboid(self.vertical_plate)
        glEnd()
        glPopMatrix()
        self.update()

    def update(self):
        if self.curr_height < self.target_height and self.curr_height < self.max_height:
            self.curr_height += 0.001 * 3

        if self.curr_height > self.target_height and self.curr_height > 0:
            self.curr_height -= 0.001 * 3

        if self.target_height < 0:
            self.target_height = 0

        if self.target_height > self.max_height:
            self.target_height = self.max_height
