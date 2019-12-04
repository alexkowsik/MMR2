import sys

import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


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
        self.fx = [None] * WIDTH
        self.lambda_sin = []
        self.lambda_cos = []
        self.f_dach = []

    def fourier_transformation(self):
        print("starting fourier transformation")
        start = None
        start_actual = None
        end = None
        end_actual = None
        length = None

        for x, f_x in enumerate(self.fx):
            if f_x is not None:
                start_actual = x + 1
                start = 2 * np.pi / start_actual
                break

        for x, f_x in enumerate(self.fx[start_actual:]):
            if f_x is None:
                end_actual = start_actual + x - 1
                end = 2 * np.pi / end_actual
                break

        length = end_actual - start_actual

        for i in range(length):
            l_sin = 0
            l_cos = 0

            for i in range(length):
                l_sin += np.sin(i * (start + i / length)) * \
                    self.fx[start_actual + i]
                l_cos += np.cos(i * (start + i / length)) * \
                    self.fx[start_actual + i]

            self.lambda_sin.append(2 * np.pi * l_sin / length)
            self.lambda_cos.append(2 * np.pi * l_cos / length)

        for i in range(length):
            self.f_dach.append(0)

            for m in range(length):
                self.f_dach[i] += self.lambda_sin[m] * np.sin(m * i)
                self.f_dach[i] += self.lambda_cos[m] * np.cos(m * i)

        print("finished fourier transformation")
        self.draw_f_dach(start_actual, end_actual)

    def read_curve_from_img(self):
        for i in range(WIDTH):
            for j in range(HEIGTH):
                if self.img.pixel(i, j):
                    self.fx[i] = j
                    break

    def draw_f_dach(self, start, end):
        self.painter.setPen(QPen(Qt.red, 1))

        for i in range(start, end):
            self.painter.drawPoint(i, self.f_dach[i - start])

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
        self.fx = [None] * WIDTH
        self.lambda_sin = []
        self.lambda_cos = []
        self.f_dach = []

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
