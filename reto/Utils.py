from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


def Axis():
    glShadeModel(GL_FLAT)
    glBegin(GL_LINES)

    # X axis in red
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-500, 0.0, 0.0)
    glVertex3f(500, 0.0, 0.0)

    # Y axis in green
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, 500, 0.0)
    glVertex3f(0.0, -500, 0.0)

    # Z axis in blue
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, 500)
    glVertex3f(0.0, 0.0, -500)

    glEnd()
    glLineWidth(3)


def plane(width: float, length: float, height: float, color: list[float], texture_id):
    points = [
        [-width, height, -length],
        [-width, height, length],
        [width, height, length],
        [width, height, -length],
    ]

    # Activar y enlazar la textura
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glPushMatrix()
    glColor3fv(color)
    glBegin(GL_QUADS)

    # Asignar coordenadas de textura a cada vértice
    glTexCoord2f(0.0, 0.0)
    glVertex3fv(points[0])
    glTexCoord2f(1.0, 0.0)
    glVertex3fv(points[1])
    glTexCoord2f(1.0, 1.0)
    glVertex3fv(points[2])
    glTexCoord2f(0.0, 1.0)
    glVertex3fv(points[3])

    glEnd()
    glPopMatrix()

    # Desactivar el uso de texturas
    glDisable(GL_TEXTURE_2D)

    
def horizons(width: float, length: float, height: float, colors: list[list[float]], texture_id):
    # Asegurarse de que hay un color para cada pared
    if len(colors) != 4:
        raise ValueError("Se requieren exactamente 4 colores, uno para cada pared")

    # Puntos de las paredes
    frontWall = [
        [-width, height, length],
        [width, height, length],
        [width, 0, length],
        [-width, 0, length],
    ]

    backWall = [
        [-width, height, -length],
        [width, height, -length],
        [width, 0, -length],
        [-width, 0, -length],
    ]

    leftWall = [
        [-width, height, -length],
        [-width, height, length],
        [-width, 0, length],
        [-width, 0, -length],
    ]

    rightWall = [
        [width, height, -length],
        [width, height, length],
        [width, 0, length],
        [width, 0, -length],
    ]

    walls = [frontWall, backWall, leftWall, rightWall]

    # Activar y enlazar la textura
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    # Dibujar cada pared con la textura aplicada
    for wall in walls:
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)  # Cambiado para voltear la textura
        glVertex3fv(wall[0])
        glTexCoord2f(1.0, 0.0)  # Cambiado
        glVertex3fv(wall[1])
        glTexCoord2f(1.0, 1.0)
        glVertex3fv(wall[2])
        glTexCoord2f(0.0, 1.0)
        glVertex3fv(wall[3])
        glEnd()

    # Desactivar el uso de texturas
    glDisable(GL_TEXTURE_2D)