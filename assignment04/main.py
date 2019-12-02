import sys

import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


WIDTH, HEIGTH = 500, 500


def p1(t):
    return (1/6) * t**3


def p2(t):
    return (1/6) * (1 + 3 * t + 3 * (t**2) - 3 * (t**3))


def p3(t):
    return (1/6) * (4 - 6 * (t**2) + 3 * (t**3))


def p4(t):
    return (1/6) * (1 - 3 * t + 3 * (t**2) - (t**3))


def b(t):
    if t < 0:
        return 0
    elif t <= 1:
        return p1(t)
    elif t <= 2:
        return p2(t - 1)
    elif t <= 3:
        return p3(t - 2)
    elif t <= 4:
        return p4(t - 3)
    else:
        return 0


def b_spline(x):
    return [b(t) for t in x]


def b_spline_with_points(x, points):
    res_x = []
    res_y = []

    for i in range(len(x) - 1):
        fx = 0
        fy = 0

        for j in range(4):
            fx += points[j][0] * b(x[i] - j)
            fy += points[j][1] * b(x[i] - j)
        res_x.append(fx)
        res_y.append(fy)

    return res_x, res_y


class Interpolation():

    def __init__(self):
        self.display = QLabel()
        self.img = QImage(WIDTH, HEIGTH, QImage.Format_RGBA8888)
        self.painter = QPainter(self.img)
        self.display.setPixmap(QPixmap.fromImage(self.img))
        self.display.show()
        self.display.mousePressEvent = self.mouse_press
        self.points = []
        self.points_drawn = 0
        self.x = np.linspace(0, 5, 501)

    def drawPoint(self, x, y):
        print(self.points, self.points_drawn)

        if self.points_drawn == 0:
            self.img.fill(0)

        self.points.append([x, y])
        self.points_drawn += 1
        self.painter.setPen(QPen(Qt.black, 10))
        self.painter.drawPoint(x, y)

        if self.points_drawn == 4:
            self.draw_function()

        self.display.setPixmap(QPixmap.fromImage(self.img))
        self.display.show()

    def draw_function(self):
        points = []

        for i in range(4):
            px = 5 * self.points[i][0] / WIDTH
            py = 5 * self.points[i][1] / HEIGTH
            points.append([px, py])

        fx, fy = b_spline_with_points(self.x, points)

        self.painter.setPen(QPen(Qt.black, 3))
        for i in range(len(fx) - 1):
            self.painter.drawPoint(fx[i] * WIDTH / 5, fy[i] * HEIGTH / 5)

        self.display.setPixmap(QPixmap.fromImage(self.img))
        self.display.show()
        self.points_drawn = 0
        self.points = []

    def mouse_press(self, event):
        pos = event.pos()
        self.drawPoint(pos.x(), pos.y())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    x = np.linspace(0, 5, 501)
    i = 1

    # plot Gaussian Function
    # plt.plot(x, 0.564 * np.exp(-(x - i)**2))

    # plot b-splines
    # plt.plot(x, b_spline(x))

    # plot b-splines with control points
    # points = [[0, 1], [1, 2], [2, 0], [3, 1]]
    # x_vals, y_vals = b_spline_with_points(x, points)
    # plt.plot(x_vals, y_vals)

    # plt.show()

    I = Interpolation()

    app.exec()
