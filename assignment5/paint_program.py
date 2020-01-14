import sys

import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt

#Params

WIDTH, HEIGTH = 1000, 1000
num_segments = 15

#this implements the drawing program, that copies what is drawn in a segment and repeats it across all other
#segments.
#The framwork was stolen from our FourierBase assignment
class Crystal():

    def __init__(self):
        self.display = QLabel()
        self.img = QImage(WIDTH, HEIGTH, QImage.Format_RGBA8888)
        self.img.fill(0)
        self.painter = QPainter(self.img)
        self.display.setPixmap(QPixmap.fromImage(self.img))
        self.display.setFixedSize(WIDTH, HEIGTH)
        self.colors = [Qt.black, Qt.green, Qt.red, Qt.cyan, Qt.blue]
        self.cur_color = self.colors[0]
        self.color_index = 0
        self.display.show()
        self.mouse_drawing = False
        self.last_point = None
        self.display.keyPressEvent = self.keyPressEvent

        #this code makes lines from the center. The angles between the lines are all equal
        self.painter.setPen(QPen(Qt.black, 2))
        if num_segments > 1:
            for k in range (1,num_segments+1):
                self.painter.drawLine(QPoint(WIDTH / 2, HEIGTH / 2), QPoint(WIDTH/2+np.cos((k*2*np.pi)/num_segments)*HEIGTH,
                                                                        HEIGTH/2+np.sin((k*-2*np.pi)/num_segments)*WIDTH))




        self.display.setPixmap(QPixmap.fromImage(self.img))
        self.display.show()

        self.display.mousePressEvent = self.mouse_press
        self.display.mouseMoveEvent = self.mouse_move
        self.display.mouseReleaseEvent = self.mouse_release







    def draw_line_to(self, p):
        #this function draws a line in all segments. The frist line is between the 2nd-last and last position
        #of the mouse: the other lines are the same, but rotated into the other segments using a rotationmatrix
        self.painter.setPen(QPen(self.cur_color, 1))
        x_old = WIDTH/2 -self.last_point.x()
        y_old = HEIGTH/2 -self.last_point.y()
        x = WIDTH/2-p.x()
        y = HEIGTH/2-p.y()
        for k in range(1,num_segments+1):
            target_x =  WIDTH/2+np.cos(np.pi+k*2*np.pi/num_segments) *x + -np.sin(np.pi+k*2*np.pi/num_segments)*y
            target_y = HEIGTH/2+np.sin(np.pi+k*2*np.pi/num_segments) *x + np.cos(np.pi+k*2*np.pi/num_segments)*y
            source_x =  WIDTH/2+np.cos(np.pi+k*2*np.pi/num_segments) *x_old + -np.sin(np.pi+k*2*np.pi/num_segments)*y_old
            source_y = HEIGTH/2+np.sin(np.pi+k*2*np.pi/num_segments) *x_old + np.cos(np.pi+k*2*np.pi/num_segments)*y_old
            self.painter.drawLine(QPoint(source_x,source_y),QPoint(target_x,target_y))
            self.display.setPixmap(QPixmap.fromImage(self.img))
            self.display.show()

        #self.painter.drawLine(self.last_point, p)
        self.last_point = p
        self.display.setPixmap(QPixmap.fromImage(self.img))


    def mouse_press(self, event):
        if event.buttons() == Qt.LeftButton:
            self.last_point = event.pos()
            self.mouse_drawing = True

    def mouse_move(self, event):
        if event.buttons() == Qt.LeftButton and self.mouse_drawing:
            p = event.pos()
            self.draw_line_to(p)

    def mouse_release(self, event):
        if self.mouse_drawing:
            self.draw_line_to(event.pos())
            self.mouse_drawing = False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_C:
            self.color_index += 1
            self.cur_color = self.colors[(self.color_index) % len(self.colors)]




if __name__ == '__main__':
    app = QApplication(sys.argv)

    F = Crystal()

    app.exec()
