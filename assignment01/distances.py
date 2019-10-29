from PyQt5 import QtGui
from PyQt5.QtCore import Qt,QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from math import sin,cos,acos,sqrt,pow
import sys
from graph import GraphAsDict
from dijkstra import dijkstra
from dijkstra_euclidian_dist_approx import dijkstra_euk
from dijkstra_landmarks_approx import dijkstra_landmarks
import csv
import timeit

g = GraphAsDict()
with open("maps/nodes.csv", newline="") as file:    #open file
    reader = csv.reader(file, delimiter=",")
    for row in reader:                                  #returns rows
        g.add_node(int(row[0]), 0, float(row[2]), float(row[1]))        #row[0]: node,[1]:breitengrad,[2]:laengengrad

with open("maps/edges.csv", newline="") as file:  # open file
    reader = csv.reader(file, delimiter=",")
    for row in reader:
        beta1 = g.nodes[int(row[0])][2]
        lambda1 = g.nodes[int(row[0])][3]
        beta2 = g.nodes[int(row[1])][2]
        lambda2 = g.nodes[int(row[1])][3]
        dist = 6378.388 * acos(sin(beta1) * sin(beta2) + cos(beta1) * cos(beta2) * cos(abs(lambda1 - lambda2)))
        g.add_edge((int(row[0]), int(row[1])), dist)
file.close()
minLaengengrad = min( [x[3] for x in g.nodes.values()] )
minBreitengrad = min([x[2] for x in g.nodes.values()])
maxLaengengrad = max([x[3] for x in g.nodes.values()])
maxBreitengrad = max([x[2] for x in g.nodes.values()])
diffLaenge = maxLaengengrad-minLaengengrad
diffBreite = maxBreitengrad-minBreitengrad

class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        print("ok")
        self.hist = []

        self.display = QLabel()

        self.title = "Dijkstra"

        self.top = 150

        self.left = 150

        self.width = 1000

        self.height = 800

        self.InitWindow()

        self.flag = False

        self.setCentralWidget(self.display)


    def InitWindow(self):

        self.setGeometry(self.top, self.left, self.width, self.height)
        self.display.setGeometry(self.top, self.left, self.width, self.height)
        ###
        painter = QtGui.QPainter(self)
        self.pixmap = QtGui.QPixmap("maps/Black.jpg").scaled(1000, 800)
        painter = QtGui.QPainter(self.pixmap)
        painter.drawPixmap(self.rect(), self.pixmap)
        pen = QtGui.QPen(Qt.white, 2)
        painter.setPen(pen)
        for node in g.nodes:
            x = ((maxLaengengrad - g.nodes[node][3]) / diffLaenge) * self.width
            y = ((maxBreitengrad - g.nodes[node][2]) / diffBreite) * self.height
            for edge in g.nodes[node][1]:
                x1 = ((maxLaengengrad - g.nodes[edge[0]][3]) / diffLaenge) * self.width
                y1 = ((maxBreitengrad - g.nodes[edge[0]][2]) / diffBreite) * self.height
                pen = QtGui.QPen(Qt.red, 1)
                painter.setPen(pen)
                painter.drawLine(QPoint(x, y), QPoint(x1, y1))
            pen = QtGui.QPen(Qt.white, 2)
            painter.setPen(pen)
            painter.drawPoint(x, y)
        ###
        self.display.setPixmap(self.pixmap)
        self.display.show()
        self.show()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self.pixmap)
        painter.drawPixmap(self.rect(), self.pixmap)
        if self.flag:
            pen = QtGui.QPen(Qt.yellow, 7)
            painter.setPen(pen)
            x = self.mousePos.x()
            y = self.mousePos.y()
            minimum = 100000.0
            for i in g.nodes:
                x1 = ((maxLaengengrad - g.nodes[i][3]) / diffLaenge) * self.width
                y1 = ((maxBreitengrad - g.nodes[i][2]) / diffBreite) * self.height
                if sqrt(pow(x1-x, 2)+pow(y1-y, 2)) < minimum:
                    minimum = sqrt(pow(x1-x, 2)+pow(y1-y, 2))
                    key = i
            if key not in self.hist:
                self.hist.append(key)
            x1 = ((maxLaengengrad - g.nodes[key][3]) / diffLaenge) * self.width
            y1 = ((maxBreitengrad - g.nodes[key][2]) / diffBreite) * self.height
            painter.drawPoint(x1, y1)

            self.display.setPixmap(self.pixmap)
            self.display.show()
            self.show()

    def mousePressEvent(self, event):
        self.mousePos = event.pos()
        self.flag = True
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_D:
            print('\n calculating...')
            if len(self.hist) > 1:
                painter = QtGui.QPainter(self.pixmap)
                # print(self.hist[-1], self.hist[-2])

                start = timeit.default_timer()
                path = dijkstra(g, self.hist[-1], self.hist[-2])[::-1]
                stop = timeit.default_timer()
                print('runtime  for dijkstra():', (start - stop) * -1, 'seconds')
                if len(path) == 0:
                    return
                # print(len(path))
                pen = QtGui.QPen(Qt.green, 3)
                painter.setPen(pen)
                for i in range(len(path)-1):
                    x1 = ((maxLaengengrad - g.nodes[path[i]][3]) / diffLaenge) * self.width
                    y1 = ((maxBreitengrad - g.nodes[path[i]][2]) / diffBreite) * self.height
                    x2 = ((maxLaengengrad - g.nodes[path[i+1]][3]) / diffLaenge) * self.width
                    y2 = ((maxBreitengrad - g.nodes[path[i+1]][2]) / diffBreite) * self.height
                    painter.drawLine(QPoint(x2, y2), QPoint(x1, y1))
                self.show()
        if event.key() == Qt.Key_F:
            print('\n calculating...')
            if len(self.hist) > 1:
                painter = QtGui.QPainter(self.pixmap)
                # print(self.hist[-1], self.hist[-2])

                start = timeit.default_timer()
                path = dijkstra_euk(g, self.hist[-1], self.hist[-2])[::-1]
                stop = timeit.default_timer()
                print('runtime  for dijkstra_euk():', (start - stop) * -1, 'seconds')

                if len(path) == 0:
                    return
                # print(len(path))
                pen = QtGui.QPen(Qt.blue, 2)
                painter.setPen(pen)
                for i in range(len(path)-1):
                    x1 = ((maxLaengengrad - g.nodes[path[i]][3]) / diffLaenge) * self.width
                    y1 = ((maxBreitengrad - g.nodes[path[i]][2]) / diffBreite) * self.height
                    x2 = ((maxLaengengrad - g.nodes[path[i+1]][3]) / diffLaenge) * self.width
                    y2 = ((maxBreitengrad - g.nodes[path[i+1]][2]) / diffBreite) * self.height
                    painter.drawLine(QPoint(x2, y2), QPoint(x1, y1))
                self.show()
        if event.key() == Qt.Key_G:
            print('\n calculating...')
            if len(self.hist) > 1:
                painter = QtGui.QPainter(self.pixmap)
                # print(self.hist[-1], self.hist[-2])

                path = dijkstra_landmarks(g, self.hist[-1], self.hist[-2])[::-1]

                if len(path) == 0:
                    return
                # print(len(path))
                pen = QtGui.QPen(Qt.blue, 2)
                painter.setPen(pen)
                for i in range(len(path)-1):
                    x1 = ((maxLaengengrad - g.nodes[path[i]][3]) / diffLaenge) * self.width
                    y1 = ((maxBreitengrad - g.nodes[path[i]][2]) / diffBreite) * self.height
                    x2 = ((maxLaengengrad - g.nodes[path[i+1]][3]) / diffLaenge) * self.width
                    y2 = ((maxBreitengrad - g.nodes[path[i+1]][2]) / diffBreite) * self.height
                    painter.drawLine(QPoint(x2, y2), QPoint(x1, y1))
                self.show()


if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())
