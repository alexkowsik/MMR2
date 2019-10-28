from PyQt5 import QtGui
from PyQt5.QtCore import Qt,QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from math import sin,cos,acos,sqrt,pow
import sys
from graph import GraphAsList, GraphAsDict
import csv
g = GraphAsDict()
with open("maps/nodes.csv",newline="") as file:    #open file
    reader = csv.reader(file,delimiter=",")
    for row in reader:                                  #returns rows
        g.add_node(int(row[0]),0 ,float(row[2]),float(row[1]))        #row[0]: node,[1]:breitengrad,[2]:laengengrad

with open("maps/edges.csv", newline="") as file:  # open file
    reader = csv.reader(file,delimiter= ",")
    for row in reader:
        beta1 =g.nodes[int(row[0])][2]
        lambda1=g.nodes[int(row[0])][3]
        beta2=g.nodes[int(row[1])][2]
        lambda2=g.nodes[int(row[1])][3]
        dist = 6378.388 * acos(sin(beta1) * sin(beta2) + cos(beta1) * cos(beta2) * cos(abs(lambda1 - lambda2)))
        g.add_edge((int(row[0]),int(row[1])),dist)
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

        self.display = QLabel()

        self.title = "PyQt5 Drawing Tutorial"

        self.top = 150

        self.left = 150

        self.width = 1366

        self.height = 768

        self.InitWindow()

        self.flag = False

        self.setCentralWidget(self.display)


    def InitWindow(self):

        self.setGeometry(self.top, self.left, self.width, self.height)
        ###
        painter = QtGui.QPainter(self)
        self.pixmap = QtGui.QPixmap("maps/Black.jpg")
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
            pen = QtGui.QPen(Qt.yellow,8)
            painter.setPen(pen)
            x = self.mousePos.x()
            y = self.mousePos.y()
            print(x,y)
            min = 100000.0
            for i in g.nodes:
                x1=((maxLaengengrad - g.nodes[i][3]) / diffLaenge) * self.width
                y1=((maxBreitengrad - g.nodes[i][2]) / diffBreite) * self.height
                if sqrt(pow(x1-x,2)+pow(y1-y,2)) < min:
                    min = sqrt(pow(x1-x,2)+pow(y1-y,2))
                    key = i
            x1 = ((maxLaengengrad - g.nodes[key][3]) / diffLaenge) * self.width
            y1 = ((maxBreitengrad - g.nodes[key][2]) / diffBreite) * self.height
            painter.drawPoint(x1,y1)
            painter.drawPoint(g.nodes[key][3],g.nodes[key][2])
            self.display.setPixmap(self.pixmap)
            self.display.show()
            self.show()

    def mousePressEvent(self, event):
        self.mousePos = event.pos()
        self.flag = True
        self.update()

if __name__ =="__main__":
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())
