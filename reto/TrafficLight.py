from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math
import random


class TrafficLight:
    def __init__(self):
        self.colors = {
            "red": (1.0, 0.0, 0.0),
            "yellow": (1.0, 1.0, 0.0),
            "green": (0.0, 1.0, 0.0),
            "blue": (0.0, 0.0, 0.5)
        }
        self.current_color = "red" # Which color is currently on.
        length = 0.6
        width = 0.4
        height = 0.15
        self.points = [
            [-length/2, -width/2, height/2],  # bottom-left-front
            [-length/2, width/2, height/2],   # top-left-front
            [length/2, width/2, height/2],    # top-right-front
            [length/2, -width/2, height/2],   # bottom-right-front
            [-length/2, -width/2, -height/2],  # bottom-left-back
            [-length/2, width/2, -height/2],   # top-left-back
            [length/2, width/2, -height/2],    # top-right-back
            [length/2, -width/2, -height/2],   # bottom-right-back
        ]
    
    def drawFaces(self):
        glBegin(GL_QUADS)
        glVertex3fv(self.points[0])
        glVertex3fv(self.points[1])
        glVertex3fv(self.points[2])
        glVertex3fv(self.points[3])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[4])
        glVertex3fv(self.points[5])
        glVertex3fv(self.points[6])
        glVertex3fv(self.points[7])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[0])
        glVertex3fv(self.points[1])
        glVertex3fv(self.points[5])
        glVertex3fv(self.points[4])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[1])
        glVertex3fv(self.points[2])
        glVertex3fv(self.points[6])
        glVertex3fv(self.points[5])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[2])
        glVertex3fv(self.points[3])
        glVertex3fv(self.points[7])
        glVertex3fv(self.points[6])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[3])
        glVertex3fv(self.points[0])
        glVertex3fv(self.points[4])
        glVertex3fv(self.points[7])
        glEnd()
    
    def draw_sphere(self, radius, slices, stacks):
        for i in range(stacks):
            lat0 = math.pi * (-0.5 + (i / stacks))
            z0 = math.sin(lat0) * radius
            zr0 = math.cos(lat0) * radius

            lat1 = math.pi * (-0.5 + ((i + 1) / stacks))
            z1 = math.sin(lat1) * radius
            zr1 = math.cos(lat1) * radius

            glBegin(GL_QUAD_STRIP)
            for j in range(slices + 1):
                lng = 2 * math.pi * (j / slices)
                x = math.cos(lng) * radius
                y = math.sin(lng) * radius

                glNormal3f(x / radius, y / radius, z0 / radius)
                glVertex3f(x, y, z0)
                
                glNormal3f(x / radius, y / radius, z1 / radius)
                glVertex3f(x, y, z1)
            glEnd()
        
    def draw(self):
        glPushMatrix()
        glScaled(5, 5, 5)
        glColor3f(1.0, 1.0, 1.0)
        self.drawFaces()
        glPopMatrix()

        # Draw lights
        for color, position in zip(self.colors.keys(), [(-0.6, 1.1, 1), (0.2, 1.1, 1), (1.0, 1.1, 1), (1.8, 1.1, 1)]):
            if color == self.current_color:
                intensity = 2.0  # Brighter if the current color
            else:
                intensity = 0.30  # Dimmer for other colors

            glColor3f(self.colors[color][0] * intensity, self.colors[color][1] * intensity, self.colors[color][2] * intensity)
            glPushMatrix()
            glTranslated(*position)
            self.draw_sphere(0.2, 50, 50)
            glPopMatrix()
