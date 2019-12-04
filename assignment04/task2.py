import sys

import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


WIDTH, HEIGTH = 800, 800


class FourierBase:

    def __init__(self):
        self.display = QLabel()
        self.img = QImage(WIDTH, HEIGTH, QImage.Format_RGBA8888)
        self.painter = QPainter(self.img)
        self.display.setPixmap(QPixmap.fromImage(self.img))
        self.display.show()
        self.mouse_drawing = False
        self.last_point = None
        self.display.mousePressEvent = self.mouse_press
        self.display.mouseMoveEvent = self.mouse_move
        self.display.mouseReleaseEvent = self.mouse_release

    def draw_line_to(self, p):
        self.painter.setPen(QPen(Qt.black, 2))
        self.painter.drawLine(
            self.last_point[0], self.last_point[1], p[0], p[1])
        self.last_point = p
        self.display.setPixmap(QPixmap.fromImage(self.img))
        self.display.show()

    def mouse_press(self, event):
        if event.buttons() == Qt.LeftButton:
            p = (event.pos().x(), event.pos().y())
            self.last_point = p
            self.mouse_drawing = True

    def mouse_move(self, event):
        if event.buttons() == Qt.LeftButton and self.mouse_drawing:
            p = (event.pos().x(), event.pos().y())
            self.draw_line_to(p)

    def mouse_release(self, event):
        if event.buttons() == Qt.LeftButton and self.mouse_drawing:
            p = (event.pos().x(), event.pos().y())
            self.draw_line_to(p)
            self.mouse_drawing = False


if __name__ == '__main__':
    app = QApplication(sys.argv)

    F = FourierBase()

    app.exec()
