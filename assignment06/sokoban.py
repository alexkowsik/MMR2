import sys

import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from copy import deepcopy
import traceback
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

    def __sub__(self, other):
        return Pos(other.x - self.x, other.y - self.y)

    def __add__(self, other):
        return Pos(other.x + self.x, other.y + self.y)

    def __str__(self):
        return str(self.x) + " " + str(self.y)

    def distance(self):
        return self.x + self.y

    def __mul__(self, other):
        return Pos(self.x * other, self.y * other)

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True

class Game:
    class GameField:
        def copy(self, other):
            self.playerPos = deepcopy(other.playerPos)
            self.boxPos = deepcopy(other.boxPos)
            self.field = deepcopy(other.field)
            self.target = deepcopy(other.target)
            self.goal = deepcopy(other.goal)

        # 0 == free, 1 == Black, 2 == box, 3 == Player
        # setup a playing field
        def __init__(self):
            self.pixmap = QPixmap(QPixmap.fromImage(
                QImage(W, H, QImage.Format_RGBA8888)))
            self.label = QLabel()
            self.field = np.zeros((N, N))
            self.playerPos = Pos(1, 1)
            self.field[1][1] = player
            self.boxPos = Pos(2, 2)
            self.field[2][2] = box
            self.target = Pos(6, N - 1)
            self.goal = 0

            self.moveCounter = 0
            for i in range(N):
                self.field[0][i] = black
                self.field[N - 1][i] = black
                self.field[i][0] = black
                self.field[i][N - 1] = black

            self.field[6][N - 1] = free
            self.goal = Pos(6, N - 1)


            # draw shizz
            self.painterInstance = QPainter(self.pixmap)
            self.penRectangle = QPen(Qt.black)
            self.penRectangle.setWidth(1)
            self.painterInstance.setPen(self.penRectangle)
            for i in range(N):
                for j in range(N):
                    if self.field[i][j] == free:
                        self.painterInstance.setBrush(
                            QBrush(Qt.white, Qt.SolidPattern))
                        self.painterInstance.drawRect(
                            j * W // N, i * H // N, W // N, H // N)
                    if self.field[i][j] == black:
                        self.painterInstance.setBrush(
                            QBrush(Qt.black, Qt.SolidPattern))
                        self.painterInstance.drawRect(
                            j * W // N, i * H // N, W // N, H // N)

            self.painterInstance.setBrush(QBrush(Qt.green, Qt.SolidPattern))
            self.painterInstance.drawEllipse(2 + self.playerPos.x * W // N, 2 + self.playerPos.y * H // N,
                                             0.8 * (W // N), 0.8 * (H // N))

            self.painterInstance.setBrush(QBrush(Qt.yellow, Qt.SolidPattern))
            self.painterInstance.drawRect(
                self.boxPos.x * W // N, self.boxPos.y * H // N, W // N, H // N)
            self.painterInstance.drawLine(self.boxPos.x * W // N, self.boxPos.y * H // N, (self.boxPos.x + 1) * W // N,
                                          (self.boxPos.y + 1) * H // N)
            self.painterInstance.drawLine((self.boxPos.x + 1) * W // N, self.boxPos.y * H // N,
                                          (self.boxPos.x) * W // N,
                                          (self.boxPos.y + 1) * H // N)

            self.painterInstance.end()
            self.label.setPixmap(self.pixmap)

        def move(self, direction):
            # directions = 2: down,6:left,8:up, 4:left
            flag = 0
            if direction == down:
                if self.playerPos.x + 1 == N or (self.boxPos.x == self.playerPos.x + 1 and self.playerPos.x + 2 == N):
                    return 0
                xDif = 1
                yDif = 0
            if direction == up:
                if self.playerPos.x - 1 == -1 or (self.boxPos.x == self.playerPos.x - 1 and self.playerPos.x - 2 == -1):
                    return 0
                xDif = -1
                yDif = 0
            if direction == left:
                if self.playerPos.y - 1 == -1 or (self.boxPos.y == self.playerPos.y - 1 and self.playerPos.y - 2 == -1):
                    return 0
                xDif = 0
                yDif = -1
            if direction == right:
                if self.playerPos.y + 1 == N or (self.boxPos.y == self.playerPos.y + 1 and self.playerPos.y + 2 == N):
                    return 0
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
                    self.painterInstance.setBrush(
                        QBrush(Qt.white, Qt.SolidPattern))
                    self.painterInstance.drawRect(
                        self.boxPos.y * W // N, self.boxPos.x * H // N, W // N, H // N)
                    self.painterInstance.setBrush(
                        QBrush(Qt.green, Qt.SolidPattern))
                    self.painterInstance.drawEllipse(2 + self.boxPos.y * W // N, 2 + self.boxPos.x * H // N,
                                                     0.8 * (W // N), 0.8 * (H // N))

                    self.boxPos.x += xDif
                    self.boxPos.y += yDif
                    self.field[self.boxPos.x][self.boxPos.y] = box
                    self.painterInstance.setBrush(
                        QBrush(Qt.yellow, Qt.SolidPattern))
                    self.painterInstance.drawRect(
                        self.boxPos.y * W // N, self.boxPos.x * H // N, W // N, H // N)
                    self.painterInstance.drawLine(self.boxPos.y * W // N, self.boxPos.x * H // N,
                                                  (self.boxPos.y + 1) * W // N,
                                                  (self.boxPos.x + 1) * H // N)
                    self.painterInstance.drawLine((self.boxPos.y + 1) * W // N, self.boxPos.x * H // N,
                                                  (self.boxPos.y) * W // N,
                                                  (self.boxPos.x + 1) * H // N)

                    self.field[self.playerPos.x][self.playerPos.y] = free
                    self.painterInstance.setBrush(
                        QBrush(Qt.white, Qt.SolidPattern))
                    self.painterInstance.drawRect(
                        self.playerPos.y * W // N, self.playerPos.x * H // N, W // N, H // N)

                    self.playerPos.y += yDif
                    self.playerPos.x += xDif
                    if self.boxPos.x == 0 or self.boxPos.x == N - 1 or self.boxPos.y == 0 or self.boxPos.y == N - 1:
                        flag = 1

                else:
                    # black block im weg; box und spieler bleiben wo sie sind
                    pass
            elif (self.field[self.playerPos.x + xDif][self.playerPos.y + yDif] == black):
                pass
            # keine Box im weg
            elif (self.field[self.playerPos.x + xDif][self.playerPos.y + yDif] == free):
                self.field[self.playerPos.x][self.playerPos.y] = free
                self.painterInstance.setBrush(
                    QBrush(Qt.white, Qt.SolidPattern))
                self.painterInstance.drawRect(
                    self.playerPos.y * W // N, self.playerPos.x * H // N, W // N, H // N)
                self.playerPos.y += yDif
                self.playerPos.x += xDif
                self.field[self.playerPos.x][self.playerPos.y] = player
                self.painterInstance.setBrush(
                    QBrush(Qt.green, Qt.SolidPattern))
                self.painterInstance.drawEllipse(2 + self.playerPos.y * W // N, 2 + self.playerPos.x * H // N,
                                                 0.8 * (W // N), 0.8 * (H // N))
            self.painterInstance.end()
            self.label.setPixmap(self.pixmap)
            if not Game.is_possible(self):
                print("Not possible or win")
            return flag

    # ablauf: Setup pix, assign pix to label, add label to layout
    def __init__(self):
        self.gamesCompleted = 0
        self.uwon = 0
        self.topLeft = self.GameField()
        self.topRight = self.GameField()
        self.botLeft = self.GameField()
        self.botRight = self.GameField()

        self.widget = QWidget()  # our form of representation
        # press S to interrupt the calculations and get a result
        self.widget.keyPressEvent = self.keyPressEvent
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
            self.gamesCompleted += self.botRight.move(down)
            self.gamesCompleted += self.topRight.move(down)
            self.gamesCompleted += self.botLeft.move(down)
            self.gamesCompleted += self.topLeft.move(down)


        if event.key() == Qt.Key_W:
            self.gamesCompleted += self.botRight.move(up)
            self.gamesCompleted += self.topRight.move(up)
            self.gamesCompleted += self.botLeft.move(up)
            self.gamesCompleted += self.topLeft.move(up)

        if event.key() == Qt.Key_A:
            self.gamesCompleted += self.botRight.move(left)
            self.gamesCompleted += self.topRight.move(left)
            self.gamesCompleted += self.botLeft.move(left)
            self.gamesCompleted += self.topLeft.move(left)

        if event.key() == Qt.Key_D:
            self.gamesCompleted += self.botRight.move(right)
            self.gamesCompleted += self.topRight.move(right)
            self.gamesCompleted += self.botLeft.move(right)
            self.gamesCompleted += self.topLeft.move(right)

        if event.key() == Qt.Key_R:
            self.automaticSolving(2, self.topRight, self.topLeft)

        if self.gamesCompleted == 4:
            self.uwon += 1
            if self.uwon < 20:
                print("u win")
            elif self.uwon >= 20 and self.uwon < 40:
                print("now stop")
            elif self.uwon >= 40:
                print("stop")

    def makeLocalGraph(self, lenArg, *arg):
        # one graph solution, arg is the gamefiled passed
        graph = []
        graphstates = []
        tempdict = {
            up: Pos(-1, 0),
            down: Pos(1, 0),
            left: Pos(0, -1),
            right: Pos(0, 1)
        }
        for j in [up, down, left, right]:

            graphstates.append(j)
            for i in range(lenArg):
                temp = self.GameField()
                temp.copy(arg[i])
                temp.playerPos = temp.playerPos + tempdict[j]
                temp.boxPos = temp.boxPos + tempdict[j]
                if not Game.is_possible(temp) or temp.field[temp.playerPos.x][temp.playerPos.y] == black:
                    graphstates = []
                    print("detected that box or player cant go this way")
                    continue
                # new player pos, new boxpos, distance fom box to goal

                graphstates.append((tempdict[j] + arg[i].playerPos, tempdict[j] + arg[i].boxPos,
                                    (tempdict[j] + arg[i].boxPos - arg[i].goal).distance()))
            if len(graphstates) != 0:
                graph.append(graphstates)
            graphstates = []
        return graph

    def automaticSolving(self, numGames, *arg):
        tempdict = {
            up: Pos(-1, 0),
            down: Pos(1, 0),
            left: Pos(0, -1),
            right: Pos(0, 1)
        }
        graph = self.makeLocalGraph(numGames, *arg)
        print(graph)
        distances = []
        for direction in graph:
            for i in range(1, len(direction)):
                distances.append((direction[0], direction[i][2]))
        distances = sorted(distances, key=(lambda x: x[1]), reverse=False)

        for direction in distances:
            for i in range(numGames):
                # if player isnt behind the box regarding the optimal path
                if arg[i].playerPos == tempdict[direction[0]] - arg[i].boxPos:
                    print("got here")
                    return self.shoveBox(direction[0])
                else:
                    # self.walkBehindBox()
                    pass

    def walkBehindBox(self, numgraphs, distances):

        tempdict = {
            up: Pos(-1, 0),
            down: Pos(1, 0),
            left: Pos(0, -1),
            right: Pos(0, 1)
        }

    def shoveBox(self, direction):
        self.topLeft.move(direction)
        self.topRight.move(direction)
        self.botLeft.move(direction)
        self.botRight.move(direction)

    def is_possible(currentGame):
        x, y = currentGame.boxPos.x, currentGame.boxPos.y

        # False on win
        if currentGame.boxPos == currentGame.target:
            return False

        # False if box is in a corner
        if y - 1 >= 0:
            if currentGame.field[x][y - 1] == black:
                if x + 1 < N and x - 1 >= 0:
                    if currentGame.field[x + 1][y] == black or currentGame.field[x - 1][y] == black:
                        return False
        if y + 1 < N:
            if currentGame.field[x][y + 1] == black:
                if x + 1 < N and x - 1 >= 0:
                    if currentGame.field[x + 1][y] == black or currentGame.field[x - 1][y] == black:
                        return False

        # True if box is in a tunnel
        if (currentGame.field[x - 1][y] == currentGame.field[x + 1][y] and currentGame.field[x - 1][y] == black) \
                or (currentGame.field[x][y - 1] == currentGame.field[x][y - 1] and currentGame.field[x][y + 1] == black):
            return True

        # False if box is at a wall and cannot be moved away
        if currentGame.field[x][y - 1] == black:
            if sum(row[y - 1] for row in currentGame.field) > N - 2:
                return False
        if currentGame.field[x][y + 1] == black:
            if sum(row[y + 1] for row in currentGame.field) > N - 2:
                return False
        if currentGame.field[x - 1][y] == black:
            if sum(currentGame.field[x - 1]) > N - 2:
                return False
        if currentGame.field[x + 1][y] == black:
            if sum(currentGame.field[x + 1]) > N - 2:
                return False

        # False if box is at outer wall and target is not on that side
        if y == 1:
            if currentGame.target.y != 0:
                return False
        if y == N - 2:
            if currentGame.target.y != N - 1:
                return False
        if x == 1:
            if currentGame.target.x != 0:
                return False
        if x == N - 2:
            if currentGame.target.x != N - 1:
                return False

        return True


if __name__ == '__main__':
    app = QApplication(sys.argv)

    F = Game()

    app.exec()
