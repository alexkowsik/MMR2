import numpy as np


class VolumetricObject:

    def __init__(self):
        self.vertices = np.array()
        self.polygons = np.array([])  # numbers in self.polygons represent indices in self.vertices
        self.numOfVertices = 0
        self.numOfPolygons = 0

    def add_vertex(self, x, y, z):
        self.vertices.append([x, y, z])

    def add_polygon(self, arr):
        self.polygons.append(arr)
