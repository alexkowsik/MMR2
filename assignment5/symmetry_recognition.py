import sys

import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from random import *

# Params

WIDTH, HEIGTH = 1000, 1000


class Recognition():

    def __init__(self):
        seed()
        self.image1 = QPixmap('a.jpg')
        self.image2 = QPixmap('b.jpg')

        self.t1 = QLabel()
        self.t1.setPixmap(self.image1)

        self.t2 = QLabel()
        self.t2.setPixmap(self.image2)

        self.patches = []
        self.patches.append(self.t1)
        self.patches.append(self.t2)


        #create a layout and add images to it


        self.widget = QWidget()
        self.widget.keyPressEvent = self.keyPressEvent
        self.box = QHBoxLayout()

        for image in self.patches:
            self.box.addWidget(image)

        self.widget.setLayout(self.box)
        #self.widget.show()

    #####
        self.naive_patch_compare('test.png',6)






    def naive_patch_compare(self,tar,w):
        self.source = QPixmap(tar)
        r1 = random()
        r2 = random()
        self.patch_x = (r1 * self.source.width()) // w
        self.patch_y = (r2 * self.source.height()) // w
        self.patch_rect = QRect(self.patch_x*w,self.patch_y*w,self.patch_x*(w+1),self.patch_y*(w+1))
        self.patch = self.source.copy(self.patch_rect)
        self.t1 = QLabel()
        self.t2 = QLabel()
        self.t1.setPixmap(self.source)
        self.t2.setPixmap(self.patch)
        self.t1.show()
        self.t2.show()
        print(self.source.size())
        print(self.patch.size())
        print(r1 * self.source.width() , " ", r2 * self.source.height())
        print(self.patch_x, " ",self.patch_y)

    def mouse_press(self, event):
        pass

    def mouse_move(self, event):
        pass

    def mouse_release(self, event):
        pass

    def keyPressEvent(self,event):
        if event.key() == Qt.Key_S:
            print("ok")




if __name__ == '__main__':
    app = QApplication(sys.argv)

    F = Recognition()

    app.exec()


##############codeschnipsel#########

        # ##Combine 2 pixmaps into one################################################################################
        # self.pm = QPixmap(self.image1.width() + self.image2.width(), self.image1.height() + self.image2.height())
        #
        # self.label = QLabel()
        #
        # left = QRectF(0, self.image1.height() / 2, self.image1.width(), self.image1.height())
        # right = QRectF(self.image1.width(), self.image2.height() / 2, self.image2.width(), self.image2.height())
        # painter = QPainter(self.pm)
        # painter.drawPixmap(left, self.image1, QRectF(self.image1.rect()))
        # painter.drawPixmap(right, self.image2, QRectF(self.image2.rect()))
        #
        # self.label.setPixmap(self.pm)
        # self.label.show()
        # #end combine 2 pixmaps into one##################################