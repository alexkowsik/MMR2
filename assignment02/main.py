import sys
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


WIDTH, HEIGHT = 400, 400


class VolumetricObject:

    def __init__(self):
        self.vertices = np.empty((0, 3), dtype=int)  # vertex is list [x, y, z]
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
        self.objects = list()  # holds all objects in scene

        self.display.setPixmap(QPixmap.fromImage(self.img))
        self.display.show()

    # adds object to scene
    def add_object(self, obj):
        self.objects.append(obj)
        self.draw()  # redraw whole scene

    # draws all objects to self.img
    def draw(self):
        for obj in self.objects:
            for polygon in obj.polygons:
                vertices = obj.vertices[polygon - 1]  # vertices of current polygon
                proj_pol = self.oblique_projection(vertices)  # projected polygon QPolygonF
                # proj_pol = self.perspective_projection(vertices)

                self.painter.drawPolygon(proj_pol)
        # sets pixmap for new scene
        self.display.setPixmap(QPixmap.fromImage(self.img))
        self.display.show()

    # oblique projection as described in explanation no. 2
    @staticmethod
    def oblique_projection(vertices):
        polygon = QPolygonF()

        # factor 10 instead of 2 for better visual and +60/+40 to center the object on the image
        for vertex in vertices:
            polygon.append(QPointF(vertex[0] - 0.5 * np.sqrt(10 * vertex[2]) + 60,
                                   vertex[1] + 0.5 * np.sqrt(10 * vertex[2]) + 40))
        return polygon

    # perspective projection
    @staticmethod
    def perspective_projection(vertices):
        polygon = QPolygonF()
        a = 200

        for vertex in vertices:
            polygon.append(QPointF(vertex[0] / (vertex[2] / a + 1) + 50,
                                   vertex[1] / (vertex[2] / a + 1) + 50))
        return polygon


# class to quickly create basic objects
class TemplateObjects:

    @staticmethod
    def create_standard_cube():
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
        return obj


if __name__ == '__main__':
    app = QApplication(sys.argv)

    templates = TemplateObjects
    cube = templates.create_standard_cube()

    M = Modeling()
    M.add_object(cube)

    app.exec()
