import sys

import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt

H = 200
W = 200
N = 9
free = 0
black = 1
box = 2
player = 3
callToRevert = -1
left = 4
right = 6
up = 8
down = 2


class Pos:
    def __init__(self, a, b):
        self.x = a
        self.y = b

    def __str__(self):
        return str(self.x) + " " + str(self.y)

class Game:
    class GameField:
        # 0 == free, 1 == Black, 2 == box, 3 == Player
        # setup a playing field
        def __init__(self):
            self.pixmap = QPixmap(QPixmap.fromImage(QImage(W, H, QImage.Format_RGBA8888)))
            self.label = QLabel()
            self.field = np.zeros((N, N))
            self.playerPos = Pos(1, 1)
            self.field[1][1] = player
            self.boxPos = Pos(2, 2)
            self.field[2][2] = box

            self.moveCounter = 0
            for i in range(N):
                self.field[0][i] = black
                self.field[N - 1][i] = black
                self.field[i][0] = black
                self.field[i][N - 1] = black

            self.field[6][N - 1] = free

            # draw shizz
            self.painterInstance = QPainter(self.pixmap)
            self.penRectangle = QPen(Qt.black)
            self.penRectangle.setWidth(1)
            self.painterInstance.setPen(self.penRectangle)
            for i in range(N):
                for j in range(N):
                    if self.field[i][j] == free:
                        self.painterInstance.setBrush(QBrush(Qt.white, Qt.SolidPattern))
                        self.painterInstance.drawRect(j * W // N, i * H // N, W // N, H // N)
                    if self.field[i][j] == black:
                        self.painterInstance.setBrush(QBrush(Qt.black, Qt.SolidPattern))
                        self.painterInstance.drawRect(j * W // N, i * H // N, W // N, H // N)

            self.painterInstance.setBrush(QBrush(Qt.green, Qt.SolidPattern))
            self.painterInstance.drawEllipse(2 + self.playerPos.x * W // N, 2 + self.playerPos.y * H // N,
                                             0.8 * (W // N), 0.8 * (H // N))

            self.painterInstance.setBrush(QBrush(Qt.yellow, Qt.SolidPattern))
            self.painterInstance.drawRect(self.boxPos.x * W // N, self.boxPos.y * H // N, W // N, H // N)
            self.painterInstance.drawLine(self.boxPos.x * W // N, self.boxPos.y * H // N, (self.boxPos.x + 1) * W // N,
                                          (self.boxPos.y + 1) * H // N)
            self.painterInstance.drawLine((self.boxPos.x + 1) * W // N, self.boxPos.y * H // N,
                                          (self.boxPos.x) * W // N,
                                          (self.boxPos.y + 1) * H // N)

            self.painterInstance.end()
            self.label.setPixmap(self.pixmap)

        def move(self, direction):
            # directions = 2: down,6:left,8:up, 4:left
            if direction == down:
                if self.playerPos.x + 1 == N or (self.boxPos.x == self.playerPos.x + 1 and self.playerPos.x + 2 == N):
                    return
                xDif = 1
                yDif = 0
            if direction == up:
                if self.playerPos.x - 1 == -1 or (self.boxPos.x == self.playerPos.x - 1 and self.playerPos.x - 2 == -1):
                    return
                xDif = -1
                yDif = 0
            if direction == left:
                if self.playerPos.y - 1 == -1 or (self.boxPos.y == self.playerPos.y - 1 and self.playerPos.y - 2 == -1):
                    return
                xDif = 0
                yDif = -1
            if direction == right:
                if self.playerPos.y + 1 == N or (self.boxPos.y == self.playerPos.y + 1 and self.playerPos.y + 2 == N):
                    return
                xDif = 0
                yDif = 1

            self.painterInstance = QPainter(self.pixmap)
            self.penRectangle = QPen(Qt.black)
            self.penRectangle.setWidth(1)
            self.painterInstance.setPen(self.penRectangle)
            if self.field[self.playerPos.x + xDif][self.playerPos.y + yDif] == box:
                # box im weg
                if self.field[self.playerPos.x + (xDif * 2)][self.playerPos.y + (yDif * 2)] == free:
                    # box kann bewegt werden
                    self.field[self.boxPos.x][self.boxPos.y] = player
                    self.painterInstance.setBrush(QBrush(Qt.white, Qt.SolidPattern))
                    self.painterInstance.drawRect(self.boxPos.y * W // N, self.boxPos.x * H // N, W // N, H // N)
                    self.painterInstance.setBrush(QBrush(Qt.green, Qt.SolidPattern))
                    self.painterInstance.drawEllipse(2 + self.boxPos.y * W // N, 2 + self.boxPos.x * H // N,
                                                     0.8 * (W // N), 0.8 * (H // N))

                    self.boxPos.x += xDif
                    self.boxPos.y += yDif
                    self.field[self.boxPos.x][self.boxPos.y] = box
                    self.painterInstance.setBrush(QBrush(Qt.yellow, Qt.SolidPattern))
                    self.painterInstance.drawRect(self.boxPos.y * W // N, self.boxPos.x * H // N, W // N, H // N)
                    self.painterInstance.drawLine(self.boxPos.y * W // N, self.boxPos.x * H // N,
                                                  (self.boxPos.y + 1) * W // N,
                                                  (self.boxPos.x + 1) * H // N)
                    self.painterInstance.drawLine((self.boxPos.y + 1) * W // N, self.boxPos.x * H // N,
                                                  (self.boxPos.y) * W // N,
                                                  (self.boxPos.x + 1) * H // N)

                    self.field[self.playerPos.x][self.playerPos.y] = free
                    self.painterInstance.setBrush(QBrush(Qt.white, Qt.SolidPattern))
                    self.painterInstance.drawRect(self.playerPos.y * W // N, self.playerPos.x * H // N, W // N, H // N)

                    self.playerPos.y += yDif
                    self.playerPos.x += xDif

                else:
                    # black block im weg; box und spieler bleiben wo sie sind
                    pass
            elif (self.field[self.playerPos.x + xDif][self.playerPos.y + yDif] == black):
                pass
            elif (self.field[self.playerPos.x + xDif][self.playerPos.y + yDif] == free):  # keine Box im weg
                self.field[self.playerPos.x][self.playerPos.y] = free
                self.painterInstance.setBrush(QBrush(Qt.white, Qt.SolidPattern))
                self.painterInstance.drawRect(self.playerPos.y * W // N, self.playerPos.x * H // N, W // N, H // N)
                self.playerPos.y += yDif
                self.playerPos.x += xDif
                self.field[self.playerPos.x][self.playerPos.y] = player
                self.painterInstance.setBrush(QBrush(Qt.green, Qt.SolidPattern))
                self.painterInstance.drawEllipse(2 + self.playerPos.y * W // N, 2 + self.playerPos.x * H // N,
                                                 0.8 * (W // N), 0.8 * (H // N))
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
            self.botRight.move(down)
            self.topRight.move(down)
            self.botLeft.move(down)
            self.topLeft.move(down)
            # call to func to redraw
            # self.painterInstance = QPainter(self.topLeft.pixmap)
            # self.penRectangle = QPen(Qt.black)
            # self.penRectangle.setWidth(1)
            # self.painterInstance.setBrush(QBrush(Qt.black, Qt.SolidPattern))
            # self.painterInstance.setPen(self.penRectangle)
            # self.painterInstance.drawRect(4 * W // N, 5 * H // N, W // N, H // N)
            # self.painterInstance.end()
            # self.topLeft.label.setPixmap(self.topLeft.pixmap)
            # just need to redraw pix to make change
            print("P", self.topLeft.playerPos)
            print("b", self.topLeft.boxPos)
        if event.key() == Qt.Key_W:
            print("W")
            self.botRight.move(up)
            self.topRight.move(up)
            self.botLeft.move(up)
            self.topLeft.move(up)
            print("P", self.topLeft.playerPos)
            print("b", self.topLeft.boxPos)

        if event.key() == Qt.Key_A:
            print("A")
            self.botRight.move(left)
            self.topRight.move(left)
            self.botLeft.move(left)
            self.topLeft.move(left)
            print("P", self.topLeft.playerPos)
            print("b", self.topLeft.boxPos)

        if event.key() == Qt.Key_D:
            print("D")
            self.botRight.move(right)
            self.topRight.move(right)
            self.botLeft.move(right)
            self.topLeft.move(right)
            print("P", self.topLeft.playerPos)
            print("b", self.topLeft.boxPos)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    F = Game()

    app.exec()
