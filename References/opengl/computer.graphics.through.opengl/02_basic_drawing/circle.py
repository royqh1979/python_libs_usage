from PyQt5 import QtWidgets,QtCore,QtGui
from OpenGL.GL import *
import math as m
import random

class MyWidget(QtWidgets.QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(500,500)
        self._num_vertices = 10
        self._center_x = 50
        self._center_y = 50
        self._r = 30

    def initializeGL(self) -> None:
        glClearColor(1,1,1,0) # background color

    def paintGL(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT)

        glColor(1,0,0)

        glBegin(GL_LINE_LOOP)
        delta = 2 * m.pi / self._num_vertices
        for  i in range(self._num_vertices):
#            glColor3f(random.uniform(0,1),random.uniform(0,1),random.uniform(0,1))
            glVertex3f(self._center_x + self._r * m.cos(i*delta),
                       self._center_y + self._r * m.sin(i*delta),0)
        glEnd()
        glFlush()

    def resizeGL(self, w: int, h: int) -> None:
        glViewport(0,0,w,h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0,100,0,100,-1,1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        if event.angleDelta().isNull():
            return
        # if event.modifiers() != QtCore.Qt.ControlModifier:
            return
        numDegrees = event.angleDelta().y() / 8;
        numSteps = numDegrees / 15
        if numSteps > 0:
            self._num_vertices += 1
            self.update()
        elif numSteps < 0 and self._num_vertices>10:
            self._num_vertices -= 1
            self.update()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = MyWidget()
    win.show()
    app.exec()