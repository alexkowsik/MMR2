# WICHTIG: Irgendwas ist mit der klasse Pos schief gelaufen.
# UM von A nach B zu kommen ,muss man in der echten welt eig B-A rechnen, mit den Pos aber A-B
# Das zu ändern, würde bedeuten, man muss auch den Halben Code Ändern
# Denn das array GameField.field mann man (glaube ich) auch genauandersrum ansprechen, als gewohnt
# Bsp: Zeilen 329 und 404 sind in sich korrekt, obwohl zeile 404 genau "falschrum" ist....
# von daher, immer testen, wenn man was schreibt ( Notiz an selbst...)

import sys

import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from copy import deepcopy
import traceback
import matplotlib.pyplot as plt

import heapq

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
        self.x = b
        self.y = a

    def __sub__(self, other):
        return Pos(other.y - self.y, other.x - self.x)

    def __add__(self, other):
        return Pos(other.y + self.y, other.x + self.x)

    def __repr__(self):
        return "(" + str(self.x) + ";" + str(self.y) + ")"

    def distance(self):
        return abs(self.x) + abs(self.y)

    def __mul__(self, other):
        return Pos(self.y * other, self.x * other)

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True

    def __abs__(self):
        return Pos(abs(self.y), abs(self.x))

    def tup(self):
        return (self.y, self.x)


class Game:
    class GameField:  # copyconstruktor für die spieldaten
        def copy(self, other):
            self.playerPos = deepcopy(other.playerPos)
            self.boxPos = deepcopy(other.boxPos)
            self.field = deepcopy(other.field)
            self.target = deepcopy(other.target)
            self.goal = deepcopy(other.goal)

        # 0 == free, 1 == Black, 2 == box, 3 == Player
        # setup a playing field
        def __init__(self, d=False, f=False, g=False, j=False):
            self.pixmap = QPixmap(QPixmap.fromImage(
                QImage(W, H, QImage.Format_RGBA8888)))
            self.label = QLabel()
            self.field = np.zeros((N, N))
            self.playerPos = Pos(1, 1)
            self.field[1][1] = player
            self.boxPos = Pos(2, 2)
            self.field[2][2] = box
            self.target = Pos(N-2, N - 1)
            self.goal = Pos(N-2, N - 1)

            self.moveCounter = 0
            for i in range(N):
                self.field[0][i] = black
                self.field[N - 1][i] = black
                self.field[i][0] = black
                self.field[i][N - 1] = black

            self.field[N-2][N - 1] = free

            if d:
                self.field = [[1, 1, 1, 1, 1, 1, 1, 4, 1],
                            [1, 0, 0, 0, 0, 0, 0, 0, 1],
                            [1, 0, 1, 1, 0, 0, 0, 0, 1],
                            [1, 0, 0, 1, 0, 0, 0, 0, 1],
                            [1, 0, 2, 1, 0, 0, 0, 0, 1],
                            [1, 0, 3, 0, 0, 0, 0, 0, 1],
                            [1, 0, 0, 1, 1, 1, 0, 0, 1],
                            [1, 0, 0, 0, 0, 0, 0, 0, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1, 1]]
                self.target = Pos(0, N-1)
                self.goal = Pos(0, N - 1)

            if f:
                self.field = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 0, 1, 0, 0, 0, 1, 1, 1],
                            [1, 0, 3, 2, 0, 0, 0, 1, 1],
                            [1, 0, 1, 1, 1, 0, 0, 0, 1],
                            [1, 0, 0, 0, 0, 0, 0, 0, 1],
                            [1, 0, 0, 0, 0, 1, 0, 0, 1],
                            [1, 0, 0, 0, 0, 1, 0, 0, 1],
                            [1, 0, 0, 0, 0, 1, 0, 0, 4],
                            [1, 1, 1, 1, 1, 1, 1, 1, 1]]
                self.target = Pos(N-2, N - 1)
                self.goal = Pos(N-2, N - 1)

            if g:
                self.field = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 0, 0, 0, 1, 0, 0, 0, 1],
                        [1, 0, 0, 0, 2, 3, 0, 1, 1],
                        [1, 0, 0, 0, 1, 0, 0, 0, 1],
                        [1, 1, 1, 1, 1, 0, 0, 0, 1],
                        [1, 0, 0, 0, 1, 0, 0, 0, 1],
                        [4, 0, 0, 0, 0, 0, 0, 1, 1],
                        [1, 0, 0, 0, 0, 0, 0, 0, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1]]
                self.target = Pos(0, N - 2)
                self.goal = Pos(0, N - 2)
                
            if j:
                self.field = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 0, 0, 0, 0, 0, 0, 0, 1],
                        [1, 0, 0, 0, 0, 0, 0, 0, 1],
                        [1, 0, 0, 0, 1, 1, 0, 0, 1],
                        [1, 1, 1, 0, 1, 0, 2, 3, 1],
                        [1, 0, 0, 0, 1, 1, 0, 0, 1],
                        [1, 0, 0, 0, 1, 0, 0, 0, 1],
                        [1, 0, 0, 0, 0, 0, 0, 1, 1],
                        [1, 1, 4, 1, 1, 1, 1, 1, 1]]
                self.target = Pos(N-1, 2)
                self.goal = Pos(N-1, 2)

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
            flag = 0  # wird benutzt, um anzuzeugen, dass eine box im ziel angekommen ist

            # folgenden 4 sektionen haben gleuchen aufbatu
            if direction == down:
                # testet, ob box oder spieler das feld verlassen würden
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

                    self.boxPos.y += yDif
                    self.boxPos.x += xDif

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
            # wenn direkt vor dem spieler ein schwarzer block ist
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
            if not Game.is_possible(self.boxPos.x, self.boxPos.y, self.target.tup(), self.field):
                print("Not possible to win")
            return flag

    # Die Nodes des Graphen
    class Node:
        def __init__(self, cost, count, tupl):
            self.cost = cost
            self.state = tupl
            self.parent = None
            self.count = count

        def __lt__(self, other):
            return self.cost < other.cost

    # setup der spielfedler und des UI
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

    @staticmethod
    def dist(x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    # Es finden bei den moveX-Methoden nur Überprüfungen statt, ob ein Zug
    # möglich ist oder ob man gegen eine Wand bzw gegen die Kiste kommt.
    # Die Heuristik d berechnet sich dabei aus der Manhatten-Distanz der Box
    # zum Ziel, der MD des Spielers zur Box (es wird also "bestraft, wenn er
    # sich von der Box entfernt") sowie dem count, das ist die Anzahl der Züge,
    # die man gebraucht hat, um hier hin zu kommen. Das ist wichtig, da damit
    # sichergestellt wird, dass es der kürzeste Weg ist.
    def moveUp(self, xP, yP, xB, yB, target, field, count):
        if (xB, yB) == target:
            return (xP, yP, xB, yB), 0

        d = self.dist(xB, yB, target[0], target[1]) + \
            self.dist(xP, yP, xB, yB) + count

        if xP - 1 < 0:
            return (xP, yP, xB, yB), d

        if field[xP - 1][yP] != black:
            d = self.dist(xB, yB, target[0], target[1]) + \
                self.dist(xP - 1, yP, xB, yB) + count
            if xP - 1 == xB:
                if yB == yP:
                    if field[xB - 1][yB] != black:
                        d = self.dist(xB - 1, yB, target[0], target[1]) + \
                            self.dist(xP - 1, yP, xB - 1, yB) + count
                        return (xP - 1, yP, xB - 1, yB), d
                    else:
                        return (xP, yP, xB, yB), d
                else:
                    return (xP - 1, yP, xB, yB), d
            else:
                return (xP - 1, yP, xB, yB), d
        else:
            return (xP, yP, xB, yB), d

    def moveDown(self, xP, yP, xB, yB, target, field, count):
        if (xB, yB) == target:
            return (xP, yP, xB, yB), 0

        d = self.dist(xB, yB, target[0], target[1]) + \
            self.dist(xP, yP, xB, yB) + count

        if xP == N - 2:
            return (xP, yP, xB, yB), d

        if field[xP + 1][yP] != black:
            d = self.dist(xB, yB, target[0], target[1]) + \
                self.dist(xP + 1, yP, xB, yB) + count
            if xP + 1 == xB:
                if yB == yP:
                    if field[xB + 1][yB] != black:
                        d = self.dist(xB + 1, yB, target[0], target[1]) + \
                            self.dist(xP + 1, yP, xB + 1, yB) + count
                        return (xP + 1, yP, xB + 1, yB), d
                    else:
                        return (xP, yP, xB, yB), d
                else:
                    return (xP + 1, yP, xB, yB), d
            else:
                return (xP + 1, yP, xB, yB), d
        else:
            return (xP, yP, xB, yB), d

    def moveLeft(self, xP, yP, xB, yB, target, field, count):
        if (xB, yB) == target:
            return (xP, yP, xB, yB), 0

        d = self.dist(xB, yB, target[0], target[1]) + \
            self.dist(xP, yP, xB, yB) + count

        if yP - 1 < 0:
            return (xP, yP, xB, yB), d

        if field[xP][yP - 1] != black:
            d = self.dist(xB, yB, target[0], target[1]) + \
                self.dist(xP, yP - 1, xB, yB) + count
            if yP - 1 == yB:
                if xB == xP:
                    if field[xB][yB - 1] != black:
                        d = self.dist(xB, yB - 1, target[0], target[1]) + \
                            self.dist(xP, yP - 1, xB, yB - 1) + count
                        return (xP, yP - 1, xB, yB - 1), d
                    else:
                        return (xP, yP, xB, yB), d
                else:
                    return (xP, yP - 1, xB, yB), d
            else:
                return (xP, yP - 1, xB, yB), d
        else:
            return (xP, yP, xB, yB), d

    def moveRight(self, xP, yP, xB, yB, target, field, count):
        if (xB, yB) == target:
            return (xP, yP, xB, yB), 0

        d = self.dist(xB, yB, target[0], target[1]) + \
            self.dist(xP, yP, xB, yB) + count

        if yP == N - 2:
            return (xP, yP, xB, yB), d

        if field[xP][yP + 1] != black:
            d = self.dist(xB, yB, target[0], target[1]) + \
                self.dist(xP, yP + 1, xB, yB) + count
            if yP + 1 == yB:
                if xB == xP:
                    if field[xB][yB + 1] != black:
                        d = self.dist(xB, yB + 1, target[0], target[1]) + \
                            self.dist(xP, yP + 1, xB, yB + 1) + count
                        return (xP, yP + 1, xB, yB + 1), d
                    else:
                        return (xP, yP, xB, yB), d
                else:
                    return (xP, yP + 1, xB, yB), d
            else:
                return (xP, yP + 1, xB, yB), d
        else:
            return (xP, yP, xB, yB), d

    def printWay(self, node):
        print("--------------")
        print(node.state)
        while node.parent:
            node = node.parent
            print(node.state)
        print("--------------")

    def getStats(self, n):
        l = ["topLeft", "topRight", "botLeft", "botRight"]
        players = []
        boxes = []
        targets = []
        fields = []

        players.append(self.topLeft.playerPos.tup())
        boxes.append(self.topLeft.boxPos.tup())
        targets.append(self.topLeft.target.tup())
        fields.append(self.topLeft.field)

        if n == 2:
            players.append(self.topRight.playerPos.tup())
            boxes.append(self.topRight.boxPos.tup())
            targets.append(self.topRight.target.tup())
            fields.append(self.topRight.field)

        if n == 3:
            players.append(self.botLeft.playerPos.tup())
            boxes.append(self.botLeft.boxPos.tup())
            targets.append(self.botLeft.target.tup())
            fields.append(self.botLeft.field)

        if n == 4:
            players.append(self.botRight.playerPos.tup())
            boxes.append(self.botRight.boxPos.tup())
            targets.append(self.botRight.target.tup())
            fields.append(self.botRight.field)

        return players, boxes, targets, fields

    # q ist eine Priority-Queue und visited enthält alle bereits besuchten states.
    def dfs(self, n=2):
        q = []
        visited = dict()

        players, boxes, targets, fields = self.getStats(n)
        d = 0
        tupl = tuple()

        for i in range(n):
            tmp = self.dist(boxes[i][0], boxes[i][1], targets[i][0], targets[i][1]) + \
                self.dist(players[i][0], players[i][1],
                          boxes[i][0], boxes[i][1])
            if tmp > d:
                d = tmp
            tupl += (players[i][0], players[i][1], boxes[i][0], boxes[i][1])

        start = self.Node(d, 0, tupl)
        q.append(start)
        heapq.heapify(q)
        count = 0

        def check_all():
            end = True
            for i in range(n):
                end = end and Game.is_possible(
                    node.state[2 + 4*i], node.state[3 + 4*i], targets[i], fields[i])
            return end

        finished = [0 for _ in range(n)]

        # Solange noch Wege möglich sind, werden sie exploriert, dabei wird immer
        # der Zug mit dem kleinsten Wert genommen, da Priority-Queue.
        while q:
            if count == 50:
                pass

            if sum(finished) == n:
                print("Iterationen:", count)
                print("Weglänge:", node.count)
                print("MD vom Anfang:", d)
                self.printWay(node)
                return True

            count += 1
            node = heapq.heappop(q)
            visited[node.state] = True

            up = tuple()
            down = tuple()
            left = tuple()
            right = tuple()

            upc = downc = leftc = rightc = 0

            for i in range(n):
                xP = node.state[0 + 4*i]
                yP = node.state[1 + 4*i]
                xB = node.state[2 + 4*i]
                yB = node.state[3 + 4*i]

                # Ist das Ende erreicht, soll der Pfad ausgegeben werden
                if (xB, yB) == targets[i]:
                    finished[i] = 1

                # Klassische Tiefensuche nach Dijkstra, es werden alle möglichen Züge
                # durchprobiert unter Bedacht der Heuristiken und je nachdem, ob sie
                # möglich sind, noch nicht besucht sind und nicht zu einen Deadlock
                # führen.
                _up, up_count = self.moveUp(
                    xP, yP, xB, yB, targets[i], fields[i], node.count)
                _down, down_count = self.moveDown(
                    xP, yP, xB, yB, targets[i], fields[i], node.count)
                _left, left_count = self.moveLeft(
                    xP, yP, xB, yB, targets[i], fields[i], node.count)
                _right, right_count = self.moveRight(
                    xP, yP, xB, yB, targets[i], fields[i], node.count)

                up += _up
                down += _down
                left += _left
                right += _right

                upc = up_count if upc > up_count else upc
                downc = down_count if down_count > downc else downc
                leftc = left_count if left_count > leftc else leftc
                rightc = right_count if right_count > rightc else rightc

            # TODO: write function to check all fields
            if not up in visited:  # and check_all():
                # print("up", up)
                up = self.Node(upc, node.count + 1, up)
                up.parent = node
                visited[up.state] = True
                heapq.heappush(q, up)
            if not down in visited:  # and check_all():
                # print("down", down)
                down = self.Node(downc, node.count + 1, down)
                down.parent = node
                visited[down.state] = True
                heapq.heappush(q, down)
            if not left in visited:  # and check_all():
                # print("left", left)
                left = self.Node(leftc, node.count + 1, left)
                left.parent = node
                visited[left.state] = True
                heapq.heappush(q, left)
            if not right in visited:  # and check_all():
                # print("right", right)
                right = self.Node(rightc, node.count + 1, right)
                right.parent = node
                visited[right.state] = True
                heapq.heappush(q, right)

            if sum(finished) == n:
                print("Iterationen:", count)
                print("Weglänge:", node.count)
                print("MD vom Anfang:", d)
                self.printWay(node)
                return True

        # Das sollte eigentlich nie erreicht werden
        print(count)
        print("no way found")
        return None

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
            self.automaticSolving(
                3, self.topRight, self.topLeft, self.botRight)

        if event.key() == Qt.Key_F:
            self.dfs()

        if self.gamesCompleted == 4:
            self.uwon += 1
            if self.uwon < 20:
                print("u win")
            elif self.uwon >= 20 and self.uwon < 40:
                print("now stop")
            elif self.uwon >= 40:
                print("stop")

    # Stand gerade: erstelle einen Graphen, wo jeder Zustand wie folgt aussieht:
    # (position des spieler aus feld1, position der box auf feld1, distanz der box zum ziel,position des spielers aus feld2, position der box auf feld2, distanz der box zum ziel,...)
    # Erstelle und verbinde jeden Zustand, der mit einem Schritt erreichbar ist. (d.h. wirft ungültige züge raus)
    # es wird berücksichtigt, dass der spieler zur box muss, bevor die distanz der box zum ziel geringer wird
    # Wenn man diesen lokalen graphen wiederholt baut und sich die schriite merkt, kann man darauf dijsktra anwenden
    # oder man geht ganz faul einfach einen schritt und guckt dann was passiert...

    # umsetzungsidee:
    # erstelle Lokalen Graph
    # Führe dann den Schritt aus, der am ehesten folgende Ordnung erfüllt:
    #   box wird in die richtige richtung geschoben > spieler nähert sich der box > box entfernt sich nicht vom ziel
    #   > spieler entfernt sich nicht zur box.

    # Zustände sind durcheine Kante verbunden, wenn für eines der tupel die spielerposition dieselbe ist oder nur in
    # x oder y sich um 1 unetrscheidet
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
        # für jeder der verfügbaren richtungen
        for j in [up, down, left, right]:

            for i in range(lenArg):
                # ------------teste, ob spielzug möglich ist----------------------------------------------
                # erstelle eine kopie des spielfelds, um spielzug zu simulieren
                temp = self.GameField()
                temp.copy(arg[i])

                temp.playerPos = temp.playerPos + tempdict[j]

                if temp.playerPos == temp.boxPos:
                    temp.boxPos = temp.boxPos + tempdict[j]
                # wenn box oder spieler in einer wand lande, oder das spiel kaputtgeht
                if not Game.is_possible(temp) or temp.field[temp.playerPos.x][temp.playerPos.y] == black or \
                        temp.field[temp.boxPos.x][temp.boxPos.y] == black:
                    # ------------ende: teste, ob spielzug möglich ist----------------------------------------
                    graphstates = []
                    break
                graphstates.append((temp.playerPos, temp.boxPos,
                                    (temp.playerPos - temp.boxPos).distance(), (temp.boxPos - temp.goal).distance()))
            if len(graphstates) != 0:
                graph.append(graphstates)
            graphstates = []
        return graph

    # versucht, die gegebenen spielfelder automatisch zu lösen
    # *arg nimmt beliebig viele spielfelder
    def automaticSolving(self, numGames, *arg):
        tempdict = {
            left: Pos(-1, 0),
            right: Pos(1, 0),
            up: Pos(0, -1),
            down: Pos(0, 1)
        }

        reversedict = {
            # man muss Pos als tupel (.tup()) aufrufen, um das dict zu benutzen
            Pos(-1, 0).tup(): left,
            Pos(1, 0).tup(): right,
            Pos(0, -1).tup(): up,
            Pos(0, 1).tup(): down
        }
        # macht graphen, für alle gegebenen felder
        graph = self.makeLocalGraph(numGames, *arg)
        for i in range(len(graph)):
            temp = graph[i]
            temp = sorted(temp, key=(lambda x: x[3]), reverse=True)
            graph[i] = temp

        temp = [x[0][3] for x in graph]
        temp2 = zip(temp, graph)
        temp2 = sorted(temp2, key=lambda x: x[0], reverse=False)
        graph = [x[1] for x in temp2]
        print(graph)
        movesThatReduceDistanceToGoal = []
        movesThatReduceDistanceToBox = []
        for direction in graph:
            for i in range(numGames):
                if direction[i][3] < (arg[i].boxPos - arg[i].goal).distance():
                    movesThatReduceDistanceToGoal.append(direction)
                if direction[i][2] < (arg[i].boxPos - arg[i].playerPos).distance():
                    movesThatReduceDistanceToBox.append(direction)
        # TODO: Anhand von graph und movesThatReduceDistanceToGoal/Box entscheiden, wo sich der spieler hinbewegen soll
        # TODO: dabei achten, dass der Spieler Aauf die Richtige Seite der Box läuft , um sie zu schubsen
        # print(movesThatReduceDistanceToGoal[0][0][0] - movesThatReduceDistanceToGoal[0][0][1])
        # arg[0].move(reversedict[(movesThatReduceDistanceToGoal[0][0][0] - movesThatReduceDistanceToGoal[0][0][1]).tup()])
        # print(arg[0].boxPos+tempdict[right])
        # print("hi", movesThatReduceDistanceToGoal)
        # print("232", movesThatReduceDistanceToBox)

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

    @staticmethod
    def is_possible(xB, yB, target, field):
        x, y = xB, yB

        # False on win
        if (xB, yB) == target:
            return True

        # False if box is in a corner
        if y - 1 >= 0:
            if field[x][y - 1] == black:
                if x + 1 < N and x - 1 >= 0:
                    if field[x + 1][y] == black or field[x - 1][y] == black:
                        return False
        if y + 1 < N:
            if field[x][y + 1] == black:
                if x + 1 < N and x - 1 >= 0:
                    if field[x + 1][y] == black or field[x - 1][y] == black:
                        return False

        # True if box is in a tunnel
        if (field[x - 1][y] == field[x + 1][y] and field[x - 1][y] == black) \
                or (field[x][y - 1] == field[x][y + 1] and field[x][y + 1] == black):
            return True

        # False if box is at a wall and cannot be moved away
        if field[x][y - 1] == black:
            if sum(row[y - 1] for row in field) > N - 1 and target[1] != y:
                return False
        if field[x][y + 1] == black:
            if sum(row[y + 1] for row in field) > N - 1 and target[1] != y:
                return False
        if field[x - 1][y] == black and target[0] != x:
            if sum(field[x:, - 1]) > N - 1:
                return False
        if field[x + 1][y] == black and target[0] != x:
            if sum(field[:, x+1]) > N - 1:
                return False

        # False if box is at outer wall and target is not on that side
        if y == 1:
            if target[1] != 0 and target[1] != 1:
                return False
        if y == N - 2:
            if target[1] != N - 1 and target[1] != N - 2:
                return False
        if x == 1:
            if target[0] != 0 and target[0] != 1:
                return False
        if x == N - 2:
            if target[0] != N - 1 and target[0] != N - 2:
                return False

        return True


if __name__ == '__main__':
    app = QApplication(sys.argv)

    F = Game()

    app.exec()
