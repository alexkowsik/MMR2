import sys
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

WIDTH = 1080
HEIGHT = 720

class CenteredObject:       # used to describe objects in 3d space by size and center

    def __init__(self):
        self.center = [0, 0, 0]
        self.diameter = 0

    def set_size(self, size):
        self.diameter = int(size)

    def set_pos(self, x_coord, y_coord, z_coord):
        self.center = [x_coord, y_coord-self.diameter//2, z_coord]

    def intersect(self, vector):    # must be overridden in subclasses
        return -1


class Cube (CenteredObject):    # cube is oriented towards the cardinal directions of the system

    def __init__(self):
        super().__init__()

    def intersect(self, vector):    # returns a distance to the intersection point and an angle for reflection
        np.linalg.solve()


class Sphere(CenteredObject):

    def __init__(self):
        super().__init__()

    def intersect(self, vector):    # returns a distance to the intersection point and an angle for reflection

class Plane(CenteredObject):

    def __init__(self):
        super().__init__()

    def intersect(self, vector):    # returns a distance to the intersection point and an angle for reflection



class Renderer:

    def __init__(self):

        self.display = QLabel()
        self.img = QImage(WIDTH, HEIGHT, QImage.Format_RGBA8888)
        self.scale = 10
        self.background = QImage(QImage.fromarray(np.ones((HEIGHT, WIDTH)).astype(np.uint8)))

        self.painter = QPainter(self.img)
        self.objects = list()  # holds all objects in scene

        self.camera_pos = np.array([1000, 700, 1000])   # position of the camera in 3D space
        self.camera_vector = np.array([-1, 0, 1])       # vector describing the viewing direction of the camera
        self.focal_length = 10
        self.sc_width = WIDTH//(100//self.scale)
        self.sc_height = HEIGHT//(100//self.scale)
        self.ray_matrix = np.array()                    # matrix of vectors pointing from the camera position to each point in a matrix positioned between the camera and the scene

        self.display.setPixmap(QPixmap.fromImage(self.img))
        self.display.show()
        self.timer = QTimer()

    def add_Object(self, thing):
        self.objects.append(thing)

    def set_scale(self, percent):
        if 0 < percent <= 100:
            self.scale = percent
        else:
            self.scale = 10
            print('Renderer: could not set scale. default is 10%')

    def render_onjects(self):
        scaled_img = np.zeros(self.sc_width, self.sc_height)
        for i in range(0, self.sc_height):
            for j in range(0, self.sc_width):
                temp_vect = self.camera_pos-self.camera_pos+self.camera_vector*self.focal_length+
                for thing in self.objects:
                    thing.intersect(temp_vect)









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

    app.exec()
