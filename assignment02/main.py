import sys
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


WIDTH, HEIGHT = 200, 200


class VolumetricObject:

    def __init__(self):
        self.vertices = np.empty((0, 3), dtype=int)
        self.polygons = np.empty((0, 4), dtype=int)  # numbers in self.polygons represent indices in self.vertices
        self.numOfVertices = 0
        self.numOfPolygons = 0

    def add_vertex(self, x, y, z):
        self.vertices = np.vstack((self.vertices, np.array([x, y, z])))
        self.numOfVertices += 1

    def add_polygon(self, arr):
        self.polygons = np.vstack((self.polygons, arr))
        self.numOfPolygons += 1


class Modeling:

    def __init__(self):
        self.display = QLabel()
        self.img = QImage(WIDTH, HEIGHT, QImage.Format_RGBA8888)
        self.painter = QPainter(self.img)
        self.objects = list()

        self.display.setPixmap(QPixmap.fromImage(self.img))
        self.display.show()

    def add_object(self, obj):
        self.objects.append(obj)

    # for now only works with cube
    def draw(self):
        for obj in self.objects:
            for polygon in obj.polygons:
                vertices = obj.vertices[polygon - 1]
                tmp = np.empty((0, 2), dtype=int)

                for vertex in vertices:
                    tmp = np.vstack((tmp, np.array([vertex[0] - 0.5 * np.sqrt(10 * vertex[2]) + 60,
                                                    vertex[1] + 0.5 * np.sqrt(10 * vertex[2]) + 40])))

                for i in range(4):
                    self.painter.drawLine(tmp[(0 + i) % 4][0], tmp[(0 + i) % 4][1], tmp[(1 + i) % 4][0],
                                          tmp[(1 + i) % 4][1])
        self.display.setPixmap(QPixmap.fromImage(self.img))
        self.display.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)

    obj = VolumetricObject()
    obj.add_vertex(0, 0, 0)
    obj.add_vertex(0, 100, 0)
    obj.add_vertex(100, 100, 0)
    obj.add_vertex(100, 0, 0)
    obj.add_vertex(0, 0, 100)
    obj.add_vertex(0, 100, 100)
    obj.add_vertex(100, 100, 100)
    obj.add_vertex(100, 0, 100)

    obj.add_polygon(np.array([1, 2, 3, 4]))
    obj.add_polygon(np.array([1, 4, 8, 5]))
    obj.add_polygon(np.array([1, 2, 6, 5]))
    obj.add_polygon(np.array([5, 6, 7, 8]))
    obj.add_polygon(np.array([3, 4, 8, 7]))
    obj.add_polygon(np.array([2, 3, 7, 6]))

    M = Modeling()
    M.add_object(obj)
    M.draw()

    app.exec()
