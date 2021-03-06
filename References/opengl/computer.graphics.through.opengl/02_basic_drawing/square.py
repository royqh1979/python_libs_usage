from PyQt5 import QtWidgets,QtGui
from OpenGL.GL import *
from OpenGL.GLU import *

class MyWidget(QtWidgets.QOpenGLWidget):
    def __init__(self):
        super().__init__(None)
        self.setFixedSize(500, 500)

    def initializeGL(self) -> None:
        glClearColor(1,1,1,0) # background color

    def paintGL(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT)
        glColor3f(0,0,0)

        glBegin(GL_POLYGON)
        glVertex3f(20.0, 20.0, 0.0)
        glVertex3f(80.0, 20.0, 0.0)
        glVertex3f(80.0, 80.0, 0.0)
        glVertex3f(20.0, 80.0, 0.0)
        glEnd()

        glFlush()


    def resizeGL(self, w: int, h: int) -> None:
        glViewport(0,0,w,h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity();
        glOrtho(0,100,0,100,-1,1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity();


if __name__=="__main__":
    app=QtWidgets.QApplication([])
    win = MyWidget()
    win.show()
    app.exec()


