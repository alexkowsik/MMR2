import sys

import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


WIDTH, HEIGHT = 200, 200


# nothing changed
class VolumetricObject:

    def __init__(self):
        # vertex is list [x, y, z]
        self.vertices = np.empty((0, 3), dtype=float)
        # numbers in self.polygons represent indices in self.vertices
        self.polygons = np.empty((0, 3), dtype=int)
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


# removed projection functions, added raytracing and intersection_test
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
        # self.draw()  # redraw whole scene

    # draws all objects to self.img
    def draw(self):
        self.img.fill(Qt.white)
        myPoly = []
        cols = []
        for obj in self.objects:
            for polygon in obj.polygons:
                myPoly.append(
                    (polygon, sum([x[2] for x in self.objects[0].vertices[polygon]])))
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
            # vertices of current polygon
            vertices = self.objects[0].vertices[myPoly[i][0]]
            # proj_pol = self.oblique_projection(vertices)  # projected polygon QPolygonF

            # 2nd param is where the eye looks at,3rd param is where the eye is
            proj_pol = self.central_projection(
                vertices, (0, 0, 0), (0, 0, -10))

            # proj_pol = self.perspective_projection(vertices)
            path = QPainterPath()
            path.addPolygon(proj_pol)
            self.painter.setBrush(QColor(cols[i][0], cols[i][1], cols[i][2]))
            self.painter.setPen(
                QPen(QColor(cols[i][0], cols[i][1], cols[i][2]), 1, Qt.SolidLine))

            # brush to color polygon of object
            self.painter.setBrush(
                QBrush(QColor(cols[i][0], cols[i][1], cols[i][2]), Qt.SolidPattern))
            self.painter.drawPath(path)
            self.painter.drawPolygon(proj_pol)

        # i = 0
        # sets pixmap for new scene
        # self.painter.end()
        self.display.setPixmap(QPixmap.fromImage(self.img))

        # test if there is any intersection
        # for i in range(-50, 20):
        #     for j in range(-50, 20):
        #         if self.intersection_test(np.array([i, j, 0]), np.array([0, 0, -1])):
        #             print("Yay", i, j)
        #             break
        self.display.show()

    def raytracing(self):
        for i in range(-80, 120):
            for j in range(-80, 120):
                col = self.intersection_test(
                    np.array([i, j, 0]), np.array([0, 0, -1]))
                self.painter.setPen(QColor(col[0], col[1], col[2]))
                self.painter.drawPoint(i + 80, j + 80)
        print("finished raytracing")
        self.display.setPixmap(QPixmap.fromImage(self.img))
        self.display.show()

    # p0 is the support vector of the line, dir_vec is the direction vector.
    # goes over every triangle in all objects and tests for intersection.
    # returns True/False by now, can easily be modified to return color of intersected triangle
    def intersection_test(self, p0, dir_vec):
        for obj in self.objects:
            for (index, triangle) in enumerate(obj.polygons):
                vertices = obj.vertices[triangle]

                # u, v are direction vectors of the plane which belongs to the triangle
                u = vertices[1] - vertices[0]
                v = vertices[2] - vertices[0]
                cross = np.cross(v, u)
                vec_length = np.linalg.norm(np.cross(u, v))
                norm_vec = cross / vec_length  # norm vector of the plane/triangle

                # distant point on line (has to be behind all objects)
                p1 = p0 + 300 * dir_vec

                # if line is parallel to plane, continue
                if np.dot(norm_vec, p0 - p1) == 0:
                    print("tis ting zero")
                    continue
                c = np.dot(norm_vec, p0 -
                           vertices[0]) / np.dot(norm_vec, p0 - p1)
                S = p0 + c * (p0 - p1)  # intersection point of line with plane

                # now check if intersection point is inside the triangle (should be right, trust...)
                # basically you solve for s and t in w = s*u + t*v
                # see here for reference: http://geomalgorithms.com/a06-_intersect-2.html
                w = S - vertices[0]

                s = (np.dot(np.dot(u, v), np.dot(w, v)) - np.dot(np.dot(v, v), np.dot(w, u))) \
                    / (np.dot(u, v) ** 2 - np.dot(np.dot(u, u), np.dot(v, v)))
                t = (np.dot(np.dot(u, v), np.dot(w, u)) - np.dot(np.dot(u, u), np.dot(w, v))) \
                    / (np.dot(u, v) ** 2 - np.dot(np.dot(u, u), np.dot(v, v)))

                # this condition needs rework
                if s < 0 or t < 0 or s+t > 1:
                    # print("nope, not in triangle", s, t)
                    continue
                else:
                    return obj.color[index]
        return np.array([0, 0, 0])

    @staticmethod
    def central_projection(vertices, centralPoint, viewPoint):
        polygon = QPolygonF()
        # centralpoint is the point our eye targets. Our eye is at location viewPoint. Lines that pass through the
        # centralpoint and where our eye is are invisble. Lines,that pass through the centralpoint and are orthogonal to
        # the line between the centralpoint adn our viewpoint, appear completely parallel to our eye
        # datatype of Centralpoint and viewPoint are tuple :(x,y,z) , where x,y,z are coordinates
        normVec = np.asarray((centralPoint[0], centralPoint[1], np.abs(centralPoint[2] - viewPoint[2])),
                             dtype=float)  # "bildtafel" is always in x-y-plane
        newBase = np.asarray(
            (np.asarray((1, 0, 0)), np.asarray((0, 1, 0)), normVec))
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


# modelled cube differently and changed polygons to triangles
class TemplateObjects:

    @staticmethod
    def create_standard_cube():
        obj = VolumetricObject()

        obj.add_vertex(-35, -7.5, -100)
        obj.add_vertex(-31.5, -25, -90)
        obj.add_vertex(-26.1, -14.4, -73.35)
        obj.add_vertex(-29.6, 3.1, -83.35)
        obj.add_vertex(-15.6, -7.3, -106.45)
        obj.add_vertex(-12.1, -24.8, -96.45)
        obj.add_vertex(-6.65, -14.2, -79.8)
        obj.add_vertex(-10.15, 3.3, -89.8)

        obj.add_polygon(np.array([0, 1, 2]), 64 +
                        np.random.choice(range(128), size=3))
        obj.add_polygon(np.array([0, 2, 3]), 64 +
                        np.random.choice(range(128), size=3))
        obj.add_polygon(np.array([0, 3, 7]), 64 +
                        np.random.choice(range(128), size=3))
        obj.add_polygon(np.array([0, 7, 4]), 64 +
                        np.random.choice(range(128), size=3))
        obj.add_polygon(np.array([0, 1, 5]), 64 +
                        np.random.choice(range(128), size=3))
        obj.add_polygon(np.array([0, 5, 4]), 64 +
                        np.random.choice(range(128), size=3))
        obj.add_polygon(np.array([4, 5, 6]), 64 +
                        np.random.choice(range(128), size=3))
        obj.add_polygon(np.array([4, 6, 7]), 64 +
                        np.random.choice(range(128), size=3))
        obj.add_polygon(np.array([2, 3, 7]), 64 +
                        np.random.choice(range(128), size=3))
        obj.add_polygon(np.array([2, 7, 6]), 64 +
                        np.random.choice(range(128), size=3))
        obj.add_polygon(np.array([1, 2, 6]), 64 +
                        np.random.choice(range(128), size=3))
        obj.add_polygon(np.array([1, 6, 5]), 64 +
                        np.random.choice(range(128), size=3))

        return obj


if __name__ == '__main__':
    app = QApplication(sys.argv)

    templates = TemplateObjects
    cube = templates.create_standard_cube()
    M = Modeling()
    M.add_object(cube)
    # M.draw()

    print("Hello World")
    M.raytracing()

    app.exec()
