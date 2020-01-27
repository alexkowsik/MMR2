import sys

import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt

H = 200
W = 200
N = 9


class Game:
    class GameField:
        # 0 == free, 1 == Black, 2 == Block, 3 == Player
        # setup a playing field
        def __init__(self):
            self.pixmap = QPixmap(QPixmap.fromImage(QImage(W, H, QImage.Format_RGBA8888)))
            self.label = QLabel()
            self.field = np.zeros((N, N))
            for i in range(N):
                self.field[0][i] = 1
                self.field[N - 1][i] = 1
                self.field[i][0] = 1
                self.field[i][N - 1] = 1

            self.field[6][N - 1] = 0

            # draw shizz
            self.painterInstance = QPainter(self.pixmap)
            self.penRectangle = QPen(Qt.black)
            self.penRectangle.setWidth(1)
            self.painterInstance.setPen(self.penRectangle)
            for i in range(N):
                for j in range(N):
                    if self.field[i][j] == 0:
                        self.painterInstance.setBrush(QBrush(Qt.white, Qt.SolidPattern))
                        self.painterInstance.drawRect(i * W // N, j * H // N, W // N, H // N)
                    if self.field[i][j] == 1:
                        self.painterInstance.setBrush(QBrush(Qt.black, Qt.SolidPattern))
                        self.painterInstance.drawRect(i * W // N, j * H // N, W // N, H // N)

            self.painterInstance.end()
            self.label.setPixmap(self.pixmap)

    # ablauf: Setup pix, assign pix to label, add label to layout
    def __init__(self):
        self.topLeft = self.GameField()
        self.topRight = self.GameField()
        self.botLeft = self.GameField()
        self.botRight = self.GameField()
        self.test = self.topLeft.label
        # self.painterInstance = QPainter(self.pix)
        # self.penRectangle = QPen(Qt.cyan)
        # self.penRectangle.setWidth(1)
        # self.painterInstance.setBrush(QBrush(Qt.black, Qt.SolidPattern))
        # self.painterInstance.setPen(self.penRectangle)
        # self.painterInstance.drawRect(0, 0, 200, 200)
        # self.painterInstance.end()

        self.widget = QWidget()  # our form of representation
        self.widget.keyPressEvent = self.keyPressEvent  # press S to interrupt the calculations and get a result
        self.box = QGridLayout()

        # add gamefields
        self.box.addWidget(self.topLeft.label, 0, 0)
        self.box.addWidget(self.topRight.label, 0, 1)
        self.box.addWidget(self.botLeft.label, 1, 0)
        self.box.addWidget(self.botRight.label, 1, 1)
        self.widget.setLayout(self.box)
        self.widget.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_S:
            print("S")
            # call to func to redraw
            self.painterInstance = QPainter(self.topLeft.pixmap)
            self.penRectangle = QPen(Qt.black)
            self.penRectangle.setWidth(1)
            self.painterInstance.setBrush(QBrush(Qt.black, Qt.SolidPattern))
            self.painterInstance.setPen(self.penRectangle)
            self.painterInstance.drawRect(4 * W // N, 5 * H // N, W // N, H // N)
            self.painterInstance.end()
            self.topLeft.label.setPixmap(self.topLeft.pixmap)
            # just need to redraw pix to make change


if __name__ == '__main__':
    app = QApplication(sys.argv)

    F = Game()

    app.exec()
