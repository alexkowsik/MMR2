import sys
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import plyfile

WIDTH, HEIGHT = 600, 600


class VolumetricObject:

    def __init__(self):
        self.vertices = np.empty((0, 3), dtype=int)  # vertex is list [x, y, z]
        self.polygons = np.empty((0, 3), dtype=int)  # numbers in self.polygons represent indices in self.vertices
        self.numOfVertices = 0
        self.numOfPolygons = 0
        self.color = np.empty((0, 3), dtype=int)

    def add_vertex(self, x, y, z):
        self.vertices = np.vstack((self.vertices, np.array([x, y, z])))
        self.numOfVertices += 1

    def add_polygon(self, arr, col):
        self.polygons = np.vstack((self.polygons, arr))
        self.color = np.vstack((self.color, (col[0], col[1], col[2])))
        self.numOfPolygons += 1


class Modeling:

    def __init__(self):
        self.display = QLabel()
        self.img = QImage(WIDTH, HEIGHT, QImage.Format_RGBA8888)
        self.painter = QPainter(self.img)
        self.objects = list()  # holds all objects in scene

        self.display.setPixmap(QPixmap.fromImage(self.img))
        self.display.show()
        self.timer = QTimer()
        self.timer.timeout.connect(self.animation)

    # adds object to scene
    def add_object(self, obj):
        self.objects.append(obj)
        self.draw()  # redraw whole scene
        self.timer.start(20)

    # draws all objects to self.img
    def draw(self):
        myPoly = []
        cols = []
        for obj in self.objects:
            for polygon in obj.polygons:
                myPoly.append((polygon, sum([x[2] for x in self.objects[0].vertices[polygon - 1]])))
            for color in obj.color:
                cols.append(color)

        temp = [x[1] for x in myPoly]
        a = zip(temp, cols, myPoly)
        a = sorted(a, key=lambda lem: lem[0])
        cols = [x[1] for x in a]
        myPoly = [x[2] for x in a]

        # myPoly.reverse()
        # i = 0
        for i in range(len(myPoly)):
            vertices = self.objects[0].vertices[myPoly[i][0] - 1]  # vertices of current polygon
            # proj_pol = self.oblique_projection(vertices)  # projected polygon QPolygonF

            # 2nd param is where the eye looks at,3rd param is where the eye is
            proj_pol = self.central_projection(vertices, (0, 0, 150), (10, 50, 0))

            # proj_pol = self.perspective_projection(vertices)
            path = QPainterPath()
            path.addPolygon(proj_pol)
            self.painter.setBrush(QColor(cols[i][0], cols[i][1], cols[i][2]))
            self.painter.setPen(QPen(QColor(cols[i][0], cols[i][1], cols[i][2]), 1, Qt.SolidLine))
            # i = i+1

            # self.painter.setBrush(QBrush(Qt.SolidPattern))  # brush to color polygon of object
            self.painter.drawPath(path)
            self.painter.drawPolygon(proj_pol)
        # i = 0
        # sets pixmap for new scene
        self.painter.end()
        self.display.setPixmap(QPixmap.fromImage(self.img))
        self.display.show()

    def rotate(self):
        phi = 3.14 / 64
        rotation_matrix_x = np.array([[np.cos(phi), 0, np.sin(phi)], [0, 1, 0], [-np.sin(phi), 0, np.cos(phi)]])

        for obj in self.objects:
            obj.vertices = obj.vertices.dot(rotation_matrix_x)
        self.img = QImage(WIDTH, HEIGHT, QImage.Format_RGBA8888)
        self.painter = QPainter(self.img)
        self.draw()

    def animation(self):
        self.rotate()

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
        viewer = (50, 15, -200)
        a = 200

        for vertex in vertices:
            polygon.append(QPointF(vertex[0] + viewer[0] / (vertex[2] - viewer[2] / a + 1) + 60,
                                   vertex[1] + viewer[1] / (vertex[2] - viewer[2] / a + 1) + 40))
        return polygon

    @staticmethod
    def central_projection(vertices, centralPoint, viewPoint):
        polygon = QPolygonF()
        # centralpoint is the point our eye targets. Our eye is at location viewPoint. Lines that pass through the
        # centralpoint and where our eye is are invisble. Lines,that pass through the centralpoint and are orthogonal to
        # the line between the centralpoint adn our viewpoint, appear completely parallel to our eye
        # datatype of Centralpoint and viewPoint are tuple :(x,y,z) , where x,y,z are coordinates
        normVec = np.asarray((centralPoint[0], centralPoint[1], np.abs(centralPoint[2] - viewPoint[2])),
                             dtype=float)  # "bildtafel" is always in x-y-plane
        newBase = np.asarray((np.asarray((1, 0, 0)), np.asarray((0, 1, 0)), normVec))
        # phi = -0.2342
        # rotation_matrix_x = np.array([[np.cos(phi), 0, np.sin(phi)], [0, 1, 0], [np.sin(phi), 0, np.cos(phi)]])
        # print(newBase)
        # newBase = newBase.dot(rotation_matrix_x)
        # print(newBase)
        newBase /= np.sqrt(np.sum(newBase[0] ** 2) +
                           np.sum(newBase[1] ** 2) +
                           np.sum(np.power(newBase[2], 2))
                           )

        # factor 10 instead of 2 for better visual and +60/+40 to center the object on the image
        if normVec[2] == 0:
            normVec[2] = 0.01
        for vertex in vertices:
            # transforming of vertex positional data to out perspective.
            newX = np.sum((vertex - centralPoint) * newBase[0])
            newY = np.sum((vertex - centralPoint) * newBase[1])
            newZ = np.sum((vertex - centralPoint) * newBase[2])

            # transforming 3d data in displayable 2d data

            polygon.append(QPointF(175 * newX / (1 - newZ / normVec[2]) + WIDTH / 2,
                                   175 * newY / (1 - newZ / normVec[2]) + HEIGHT / 2))
        return polygon


# class to quickly create basic objects
class TemplateObjects:

    @staticmethod
    def create_standard_cube():
        obj = VolumetricObject()

        obj.add_vertex(-50, -50, -50)
        obj.add_vertex(-50, 50, -50)
        obj.add_vertex(50, 50, -50)
        obj.add_vertex(50, -50, -50)
        obj.add_vertex(-50, -50, 50)
        obj.add_vertex(-50, 50, 50)
        obj.add_vertex(50, 50, 50)
        obj.add_vertex(50, -50, 50)

        obj.add_polygon(np.array([1, 2, 3, 4]), 64 + np.random.choice(range(128), size=3))
        obj.add_polygon(np.array([1, 4, 8, 5]), 64 + np.random.choice(range(128), size=3))
        obj.add_polygon(np.array([1, 2, 6, 5]), 64 + np.random.choice(range(128), size=3))
        obj.add_polygon(np.array([5, 6, 7, 8]), 64 + np.random.choice(range(128), size=3))
        obj.add_polygon(np.array([3, 4, 8, 7]), 64 + np.random.choice(range(128), size=3))
        obj.add_polygon(np.array([2, 3, 7, 6]), 64 + np.random.choice(range(128), size=3))

        # hidden box!
        for val in obj.vertices:
            obj.add_vertex(val[0] * 0.3, val[1] * 0.3, val[2] * 0.3)
        for val in obj.polygons:
            obj.add_polygon(val + 8, 64 + np.random.choice(range(128), size=3))
        return obj


def drill():
    file = plyfile.PlyData.read("drill_shaft_vrip.ply");
    obj = VolumetricObject()
    for x in file['vertex']:
        obj.add_vertex(x[0] * 10000, x[1] * 1000, x[2] * 10000)
    for x in file['face']:
        obj.add_polygon(x[0], np.random.choice(range(64), size=3))
    return obj


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # sys._excepthook = sys.excepthook
    #
    #
    # def exception_hook(exctype, value, traceback):
    #     print(exctype, value, traceback)
    #     sys._excepthook(exctype, value, traceback)
    #     sys.exit(1)
    #
    #
    # sys.excepthook = exception_hook

    # templates = TemplateObjects
    # cube = templates.create_standard_cube()
    M = Modeling()
    M.add_object(drill())

    app.exec()
    ##Change polygon size in the beginning
    ## change the param of Modeling  instance
