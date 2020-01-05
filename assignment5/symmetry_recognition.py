import sys

import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
import random
import qimage2ndarray

# Params

WIDTH, HEIGTH = 1000, 1000


class Recognition():

    def __init__(self):
        random.seed()
        self. n = 7            #number of pictures to be shown after the evaluation
        self.patches = []       #the patches, to be stored as ((x_index,y_index),number of matches)
                                #index = pixel of the source image // (w or v)
        self.distinct = False    #when True, show the top n distinct patches
        self.eval_mode = 1      #0 for hits, 1 for distances with numpy, 2 for distances with qImage.pixel(x,y)
        self.w = 110                  #width of the patches
        self.v = 120            #height of the patches
        self.src = 'cmp0.jpg'        #source image

        self.btn = QPushButton("Press to Stop")
        self.btn.setText("Press to Stop")
        self.btn.clicked.connect(lambda:self.btn_click())

        self.widget = QWidget() #our form of representation
        self.widget.keyPressEvent = self.keyPressEvent  #press S to interrupt the calculations and get a result
        self.box = QHBoxLayout()
        self.box.addWidget(self.btn)
        self.widget.setLayout(self.box)
        self.widget.show()

        self.naive_patch_compare(self.src, self.w, self.v)
        self.choose_top_patches()

        self.box.removeWidget(self.btn)
        self.btn.deleteLater()
        self.btn = None


        self.widget.setLayout(self.box)
        self.widget.show()






    #be careful to choose fitting w,v
    def naive_patch_compare(self,tar,w,v):
        #remember: (index*w,index*v) is the position of the top left pixel of a picture with size w*v
        self.flag = True            # to stop computation
        self.source = QPixmap(tar)  #base image

        #split bse image into a grid of size w*v
        #put all the indices into a list
        available_patches = []
        for i in range(self.source.width() // w):
            for j in range(self.source.height() // v):
                available_patches.append((i,j))

        #choose a random patch and compare it to all the other patches of the grid. repeat this until all patches were used
        for x in range((self.source.width()//w) * (self.source.height()//v)):
            choice = random.choice(available_patches)
            available_patches.remove(choice)

            #make a picture out of the chosen patch
            self.patch_rect = QRect(choice[0] * w, choice[1] * v, w, v)
            self.patch = self.source.copy(self.patch_rect)
            self.patch_image = self.patch.toImage()
            pa = qimage2ndarray.rgb_view(self.patch_image)
            hits = np.uint64(0)

            #compare it to all other patches
            for i in range(self.source.width()//w):
                for j in range(self.source.height()//v):
                    self.rect = QRect(i*w,j*v,w,v)
                    self.cur = self.source.copy(self.rect)
                    self.image = self.cur.toImage()
                    im = qimage2ndarray.rgb_view(self.image)

                    if self.eval_mode == 0:
                        #from the Qimage documentation: "Returns true if this image and the given image have the same contents;
                        # otherwise returns false"
                        if im == pa:
                            hits = hits+1
                    elif self.eval_mode == 1:
                        for r in range (im.shape[0]):
                            for c in range (im.shape[1]):
                                hits += np.uint64(np.power(np.subtract(im[r][c],pa[r][c]),2))
                    elif self.eval_mode == 2:
                        for r in range (w):
                            for c in range (v):
                                if np.uint64(np.power(self.patch_image.pixel(r,c)-self.image.pixel(r,c),2)//np.power(2,20))/np.iinfo(np.uint64).max \
                                        + hits/np.iinfo(np.uint64).max < 1:
                                    hits += np.uint64(np.power(self.patch_image.pixel(r,c)-self.image.pixel(r,c),2)//np.power(2,20))
                                else:
                                    hits = np.iinfo(np.uint64).max
            if self.eval_mode == 0:
                self.patches.append( ((choice[0],choice[1]),hits-1) )
            elif self.eval_mode == 1 or self.eval_mode == 2:
                self.patches.append( ( (choice[0],choice[1]),hits ) )

            print(100*(x+1)/((self.source.width()//w) * (self.source.height()//v)),"% done")
            QCoreApplication.processEvents()            #the process checks if the stop button was called
            if self.flag == False:                      #if it was called, flag is True
                self.evaluate_naive_patch_compare()
                return


        self.evaluate_naive_patch_compare()


    def mouse_press(self, event):
        pass

    def mouse_move(self, event):
        pass

    def mouse_release(self, event):
        pass

    def btn_click(self):
        self.flag = False

    def keyPressEvent(self,event):
        if event.key() == Qt.Key_S:
            print("ok")
            self.flag = False

    def evaluate_naive_patch_compare(self):
        if self.eval_mode == 0:
            self.patches = sorted(self.patches,key=lambda x:x[1],reverse = True)
        elif self.eval_mode == 1:
            self.patches = sorted(self.patches, key=lambda x: x[1][0])
        elif self.eval_mode == 2:
            self.patches = sorted(self.patches, key=lambda x: x[1])
        print(self.patches)

    def choose_top_patches(self):
        #this chooses the top n patches from the evaluation, puts them in labels and in the layout
        source = QPixmap(self.src)
        self.labels = []
        if not self.distinct:
            if not (len(self.patches) < self.n):
                for i in range(self.n):
                    rect = QRect(self.patches[i][0][0] * self.w, self.patches[i][0][1] * self.v, self.w, self.v)
                    cur = source.copy(rect)
                    self.labels.append(QLabel())
                    self.labels[-1].setPixmap(cur)
            for x in range(self.n):
                self.box.addWidget(self.labels[x])
        else:
            if not (len(self.patches) < self.n):
                rect = QRect(self.patches[0][0][0] * self.w, self.patches[0][0][1] * self.v, self.w, self.v)
                cur = source.copy(rect)
                img = cur.toImage()
                run_rect = QRect(self.patches[1][0][0] * self.w, self.patches[1][0][1] * self.v, self.w, self.v)
                run_cur = source.copy(run_rect)
                run_img = run_cur.toImage()
                self.i = 0
                j = 1
                self.lbl = QLabel()
                self.lbl.setPixmap(cur)
                self.labels.append(self.lbl)
                while (self.i < self.n and j < len(self.patches)):
                    j += 1
                    if run_img == img:
                        run_rect = QRect(self.patches[j][0][0] * self.w, self.patches[j][0][1] * self.v, self.w, self.v)
                        run_cur = source.copy(run_rect)
                        run_img = run_cur.toImage()
                    else:
                        self.i += 1
                        img = run_img

                        self.labels.append(QLabel())
                        self.labels[-1].setPixmap(run_cur)
                        run_rect = QRect(self.patches[j][0][0] * self.w, self.patches[j][0][1] * self.v, self.w, self.v)
                        run_cur = source.copy(run_rect)
                        run_img = run_cur.toImage()
                for x in range(self.i):
                    self.box.addWidget(self.labels[x])

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