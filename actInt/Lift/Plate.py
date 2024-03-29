from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np
from Box import Box

from Utils import draw_cuboid


class Plate:
    def __init__(self, color: list[float]):
        self.plate_color = color
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
        self.bottom_plate_radius = 0.711  # ((0.5 - self.bottom_plate_center[0]) ** 2 + (0.15 - self.bottom_plate_center[1]) ** 2 + (1 - self.bottom_plate_center[2]) ** 2) ** 0.5

        self.boxes = []

    def render(self):
        glPushMatrix()
        glColor3f(*self.plate_color)
        glTranslate(0, self.curr_height, 0)
        glBegin(GL_QUADS)
        draw_cuboid(self.bottom_plate)
        draw_cuboid(self.vertical_plate)
        glEnd()
        for box in self.boxes:
            box.position = [0, 0, 0.51]
            glTranslate(0, 0.51, 0)
            box.render()
            self.target_height = 0.5
        glPopMatrix()
        self.update()

    def update(self):
        if not self.boxes:
            self.target_height = 0

        if self.curr_height < self.target_height and self.curr_height < self.max_height:
            self.curr_height += 0.005 * 3

        if self.curr_height > self.target_height and self.curr_height > 0:
            self.curr_height -= 0.005 * 3

        if self.target_height < 0:
            self.target_height = 0

        if self.target_height > self.max_height:
            self.target_height = self.max_height
