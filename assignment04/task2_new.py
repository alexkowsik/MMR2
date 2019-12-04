import sys

import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt


WIDTH, HEIGTH = 800, 800


class FourierBase(QWidget):

    def __init__(self):
        self.display = QLabel()
        self.img = QImage(WIDTH, HEIGTH, QImage.Format_RGBA8888)
        self.img.fill(0)
        self.painter = QPainter(self.img)
        self.display.setPixmap(QPixmap.fromImage(self.img))
        self.display.setFixedSize(WIDTH, HEIGTH)
        self.display.show()
        self.mouse_drawing = False
        self.last_point = None
        self.display.mousePressEvent = self.mouse_press
        self.display.mouseMoveEvent = self.mouse_move
        self.display.mouseReleaseEvent = self.mouse_release
        self.fx = []  # holds the y values of drawn curve f
        self.start_index = None  # index where drawn curve starts
        self.end_index = None  # index where drawn curve ends
        self.length = None  # length of drawn curve (number of x values)
        self.lambda_sin = []  # holds coefficients lambda_sin
        self.lambda_cos = []  # holds coefficients lambda_cos
        self.f_dach = []  # y values of approximated function

    def fourier_transformation(self):
        print("starting fourier transformation")

        # start and end from descrete interval on which to evaluate
        start = 0
        end = 2 * np.pi

        length = self.end_index - self.start_index

        # compute all the coefficients
        for m in range(length):
            l_sin = 0
            l_cos = 0

            for i in range(length):
                l_sin += np.sin(m * (2 * np.pi * i / length)) * \
                    self.fx[i]
                l_cos += np.cos(m * (2 * np.pi * i / length)) * \
                    self.fx[i]

            self.lambda_sin.append(2 * np.pi * l_sin / length)
            self.lambda_cos.append(2 * np.pi * l_cos / length)

        # compute the y values (f "Dach")
        for i in range(length):
            self.f_dach.append(0)

            for m in range(length):
                self.f_dach[i] += self.lambda_sin[m] * \
                    np.sin(m * (2 * np.pi * i / length))
                self.f_dach[i] += self.lambda_cos[m] * \
                    np.cos(m * (2 * np.pi * i / length))

        print(self.f_dach)

        print("finished fourier transformation")
        self.draw_f_dach()

    # stores all the y values of drawn curve in fx
    # also the start and end of the curve (indices)
    def read_curve_from_img(self):
        for i in range(WIDTH):
            for j in range(HEIGTH):
                if self.img.pixel(i, j):
                    if self.start_index is None:
                        self.start_index = i
                    self.fx.append(j)
                    self.end_index = i
                    break
        self.length = self.end_index - self.start_index
        print(self.fx)

    def draw_f_dach(self):
        self.painter.setPen(QPen(Qt.red, 3))

        for i in range(self.length):
            self.painter.drawPoint(self.start_index + i, self.f_dach[i] % 500)

        self.display.setPixmap(QPixmap.fromImage(self.img))
        self.display.show()
        print("finished drawing")

    def draw_line_to(self, p):
        self.painter.setPen(QPen(Qt.black, 1))
        self.painter.drawLine(self.last_point, p)
        self.last_point = p
        self.display.setPixmap(QPixmap.fromImage(self.img))
        self.display.show()

    def reset(self):
        self.img.fill(0)
        self.display.setPixmap(QPixmap.fromImage(self.img))
        self.display.show()
        self.fx = []
        self.lambda_sin = []
        self.lambda_cos = []
        self.f_dach = []
        self.start_index = None
        self.end_index = None
        self.length = None

    def mouse_press(self, event):
        if event.buttons() == Qt.LeftButton:
            self.reset()
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
            self.read_curve_from_img()
            self.fourier_transformation()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    F = FourierBase()

    app.exec()
