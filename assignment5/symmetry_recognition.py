import sys

import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
import random

# Params

WIDTH, HEIGTH = 1000, 1000


class Recognition():

    def __init__(self):
        random.seed()
        self. n = 4             #number of pictures to be shown after the evaluation
        self.patches = []       #the patches, to be stored as ((x_index,y_index),number of matches)
                                #index = pixel of the source image // (w or v)
        self.distinct = True    #when True, show the top n distinct images
        self.w = 41                  #width of the patches
        self.v = 41                  #height of the patches
        self.src = 'test.png'        #source image
        self.naive_patch_compare(self.src, self.w, self.v)

        self.widget = QWidget() #our form of representation
        self.widget.keyPressEvent = self.keyPressEvent  #press S to interrup the calculations and get a result
        self.box = QHBoxLayout()

        self.choose_top_patches()

        self.widget.setLayout(self.box)
        self.widget.show()






    #be careful to choose fitting w,v
    def naive_patch_compare(self,tar,w,v):
        self.flag = True
        self.source = QPixmap(tar)

        available_patches = []
        for i in range(self.source.width() // w):
            for j in range(self.source.height() // v):
                available_patches.append((i,j))

        for x in range((self.source.width()//w) * (self.source.height()//v)):
            choice = random.choice(available_patches)
            available_patches.remove(choice)

            self.patch_rect = QRect(choice[0] * w, choice[1] * v, w, v)
            self.patch = self.source.copy(self.patch_rect)
            self.patch_image = self.patch.toImage()
            hits = 0
            for i in range(self.source.width()//w):
                for j in range(self.source.height()//v):
                    self.rect = QRect(i*w,j*v,w,v)
                    self.cur = self.source.copy(self.rect)
                    self.image = self.cur.toImage()
                    #from the Qimage documentation: "Returns true if this image and the given image have the same contents;
                    # otherwise returns false"
                    if self.image == self.patch_image:
                        hits = hits+1

            self.patches.append( ((choice[0],choice[1]),hits-1) )
            print(100*(x+1)/((self.source.width()//w) * (self.source.height()//v)),"% done")
            QCoreApplication.processEvents()
            if self.flag == False:
                self.evaluate_naive_patch_compare()
                return


        self.evaluate_naive_patch_compare()


    def mouse_press(self, event):
        pass

    def mouse_move(self, event):
        pass

    def mouse_release(self, event):
        pass

    def keyPressEvent(self,event):
        if event.key() == Qt.Key_S:
            print("ok")
            self.flag = False

    def evaluate_naive_patch_compare(self):
        self.patches = sorted(self.patches,key=lambda x:x[1],reverse = True)
        print(self.patches)

    def choose_top_patches(self):
        #this chooses the top n patches from the evaluation
        source = QPixmap(self.src)
        self.labels = []
        if not self.distinct:
            if not (len(self.patches) < self.n):
                for i in range(self.n):
                    rect = QRect(self.patches[i][0][0] * self.w, self.patches[i][0][1] * self.v, self.w, self.v)
                    cur = source.copy(rect)
                    self.labels.append(QLabel())
                    self.labels[-1].setPixmap(cur)
        else:
            if not (len(self.patches) < self.n):
                rect = QRect(self.patches[0][0][0] * self.w, self.patches[0][0][1] * self.v, self.w, self.v)
                cur = source.copy(rect)
                img = cur.toImage()
                run_rect = QRect(self.patches[1][0][0] * self.w, self.patches[1][0][1] * self.v, self.w, self.v)
                run_cur = source.copy(run_rect)
                run_img = run_cur.toImage()
                i = 0
                j = 1
                self.lbl = QLabel()
                self.lbl.setPixmap(cur)
                self.labels.append(self.lbl)
                while (i < self.n and j < len(self.patches)):
                    j += 1
                    if run_img == img:
                        run_rect = QRect(self.patches[j][0][0] * self.w, self.patches[j][0][1] * self.v, self.w, self.v)
                        run_cur = source.copy(run_rect)
                        run_img = run_cur.toImage()
                    else:
                        i += 1
                        img = run_img

                        self.labels.append(QLabel())
                        self.labels[-1].setPixmap(run_cur)
                        run_rect = QRect(self.patches[j][0][0] * self.w, self.patches[j][0][1] * self.v, self.w, self.v)
                        run_cur = source.copy(run_rect)
                        run_img = run_cur.toImage()
        for i in range(self.n):
            self.box.addWidget(self.labels[i])

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