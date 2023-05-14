import math

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PyQt5.QtWidgets import QOpenGLWidget

from utils.constants import *


class SimulationWidget(QOpenGLWidget):
    def __init__(self, parent, connection):
        super().__init__(parent=parent)
        self.__quadric = gluNewQuadric()
        gluQuadricNormals(self.__quadric, GLU_SMOOTH)
        gluQuadricTexture(self.__quadric, GL_TRUE)
        self.setMinimumSize(*SIM_WINDOW_SIZE)
        self.colors = []
        self.masses = []
        self.positions = []
        self.velocities = []
        self.emitter = connection.emitter
        self.emitter.connect(self.handle_update)
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.update)
        # self.timer.start(10)

    def handle_update(self, message):
        if message['type'] == 0:
            self.colors = message['colors']
            self.masses = message['masses']
        else:
            self.positions = message['position']
            self.velocities = message['velocity']
            self.update()

    def initializeGL(self):
        glLoadIdentity()
        glClearColor(0.05, 0.0, 0.1, 1.0)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (SIM_WINDOW_SIZE[0] / SIM_WINDOW_SIZE[1]), 0.1, 50.0)
        glViewport(0, 0, *SIM_WINDOW_SIZE)
        glTranslatef(0.0, 0.0, -5.0)
        glScalef(1, 1, 1)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glShadeModel(GL_SMOOTH)

        glMatrixMode(GL_MODELVIEW)
        gluLookAt(10 * math.sin(math.pi / 4), 10 * math.sin(math.pi / 4), 10 * math.cos(math.pi / 4),
                  0, 0, 0,
                  0, 0, 1)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLightfv(GL_LIGHT0, GL_POSITION, light_position)
        glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)

        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, material_ambient)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, material_diffuse)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, material_specular)
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, material_shininess)

        self.draw_axes()

        self.draw_bodies()

    def draw_bodies(self):
        num_bodies = len(self.positions) if self.positions is not None else 0
        for i in range(num_bodies):
            glColor3f(*self.colors[i])
            glPushMatrix()
            glTranslatef(*self.positions[i])
            gluSphere(self.__quadric, self.masses[i] ** (1 / 3), 5, 5)
            glPopMatrix()

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)

    def draw_axes(self):
        glLineWidth(1.0)
        glBegin(GL_LINES)

        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(5.0, 0.0, 0.0)

        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 5.0, 0.0)

        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 5.0)

        glEnd()
