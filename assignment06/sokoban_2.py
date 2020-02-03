import sys

# import enum
from dataclasses import dataclass

import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from copy import deepcopy

WIDTH = 400
HEIGHT = WIDTH
coupled = True
DEBUG = False

map0 = [[1, 1, 1, 1, 1, 1, 1, 4, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 2, 1, 0, 0, 0, 0, 1],
        [1, 0, 3, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 1, 1, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1]]

map1 = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 1, 1, 1],
        [1, 0, 3, 2, 0, 0, 0, 1, 1],
        [1, 0, 1, 1, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 4],
        [1, 1, 1, 1, 1, 1, 1, 1, 1]]

map2 = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 2, 3, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1],
        [4, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1]]

map3 = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 1, 0, 0, 1],
        [1, 1, 1, 0, 1, 0, 2, 3, 1],
        [1, 0, 0, 0, 1, 1, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 4, 1, 1, 1, 1, 1, 1]]

maps = [map0, map1, map2, map3]


def enum(**enums):
    return type('Enum', (), enums)


@dataclass
class Point:
    x: int
    y: int


Directions = enum(north=Point(-1, 0), east=Point(0, 1), south=Point(1, 0), west=Point(0, -1))


class Display:

    def __init__(self):
        self.games = [Sokoban(map0), Sokoban(map1), Sokoban(map2), Sokoban(map3)]
        self.widget = QWidget()
        self.widget.keyPressEvent = self.keyPressEvent
        self.box = QGridLayout()

        self.displays = [None, None, None, None]

        for i in range(4):
            self.displays[i] = self.games[i].label
            self.box.addWidget(self.displays[i], i % 2, i // 2)

        self.widget.setLayout(self.box)
        self.widget.show()

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_W or event.key() == Qt.Key_Up:
            if coupled:
                for map in self.games:
                    if not map.finished:
                        map.move(Directions.north)
                        map.refresh_widget(True)
                print("------------------")
            else:
                self.games[0].move(Directions.north)
                self.games[0].refresh_widget(True)
        self.widget.update()

        if event.key() == Qt.Key_A or event.key() == Qt.Key_Left:
            if coupled:
                for map in self.games:
                    if not map.finished:
                        map.move(Directions.west)
                        map.refresh_widget(True)
                print("------------------")
            else:
                self.games[0].move(Directions.west)
                self.games[0].refresh_widget(True)
        self.widget.update()

        if event.key() == Qt.Key_S or event.key() == Qt.Key_Down:
            if coupled:
                for map in self.games:
                    if not map.finished:
                        map.move(Directions.south)
                        map.refresh_widget(True)
                print("------------------")
            else:
                self.games[0].move(Directions.south)
                self.games[0].refresh_widget(True)
        self.widget.update()

        if event.key() == Qt.Key_D or event.key() == Qt.Key_Right:
            if coupled:
                for map in self.games:
                    if not map.finished:
                        map.move(Directions.east)
                        map.refresh_widget(True)
                print("------------------")
            else:
                self.games[0].move(Directions.east)
                self.games[0].refresh_widget(True)
        self.widget.update()


class Sokoban:

    def __init__(self, map):
        self.state = map
        self.game_size = len(self.state[0])  # all maps must be squares an have the same size!
        self.player_pos = self.get_player_pos()
        self.destination = self.get_destination()
        self.finished = False
        print(self.game_size)

        self.RGB = [Qt.white, Qt.black, Qt.yellow, Qt.green, Qt.white]
        self.pixmap = QPixmap(QPixmap.fromImage(QImage(WIDTH, HEIGHT, QImage.Format_RGBA8888)))
        self.label = QLabel()
        self.refresh_widget(False)

    def game_over(self):
        self.finished = self.state[self.destination[0]][self.destination[1]] == 2
        return self.finished

    def refresh_widget(self, partial):        # partial is a bool flag indicating to only redraw around the player
        if not self.finished:
            if DEBUG:
                print("refreshing... partial = %s" % partial)
            if self.game_over():
                partial = False
                background_color = Qt.blue
            else:
                background_color = Qt.white
            if partial:
                player_pos = self.get_player_pos()
                row_range = range(player_pos[0]-1, player_pos[0]+2)
                column_range = range(player_pos[1]-1, player_pos[1]+2)
            else:
                row_range = range(self.game_size)
                column_range = range(self.game_size)

            painterInstance = QPainter(self.pixmap)
            penRectangle = QPen(Qt.black)
            penRectangle.setWidth(1)
            painterInstance.setPen(penRectangle)

            for row_index in row_range:
                if 0 <= row_index < self.game_size:
                    for column_index in column_range:
                        if 0 <= column_index < self.game_size:
                            color_id = self.state[row_index][column_index]
                            painterInstance.setBrush(QBrush(self.RGB[color_id], Qt.SolidPattern))
                            if DEBUG and not (color_id == 1) and partial:
                                painterInstance.setBrush(QBrush(Qt.red, Qt.SolidPattern))
                            elif self.game_over() and not (color_id == 1):
                                painterInstance.setBrush(QBrush(background_color, Qt.SolidPattern))
                            if color_id == 3:
                                painterInstance.setBrush(QBrush(background_color, Qt.SolidPattern))
                                painterInstance.drawRect(column_index * WIDTH // self.game_size,
                                                         row_index * HEIGHT // self.game_size,
                                                         WIDTH // self.game_size,
                                                         HEIGHT // self.game_size)
                                if not self.game_over():
                                    painterInstance.setBrush(QBrush(self.RGB[color_id], Qt.SolidPattern))
                                painterInstance.drawEllipse(column_index * WIDTH // self.game_size + 1,
                                                            row_index * HEIGHT // self.game_size + 1,
                                                            WIDTH // self.game_size - 2,
                                                            HEIGHT // self.game_size - 2)
                            else:
                                painterInstance.drawRect(column_index * WIDTH // self.game_size,
                                                         row_index * HEIGHT // self.game_size,
                                                         WIDTH // self.game_size,
                                                         HEIGHT // self.game_size)
                                if color_id == 2:
                                    painterInstance.setBrush(QBrush(Qt.black, Qt.Dense6Pattern))
                                    painterInstance.drawRect(column_index * WIDTH // self.game_size,
                                                             row_index * HEIGHT // self.game_size,
                                                             WIDTH // self.game_size,
                                                             HEIGHT // self.game_size)
            painterInstance.end()
            self.label.setPixmap(self.pixmap)

    def get_player_pos(self):
        for i in range(self.game_size):
            for j in range(self.game_size):
                if self.state[i][j] == 3:
                    return tuple([i, j])

    def get_destination(self):
        for i in range(self.game_size):
            for j in range(self.game_size):
                if self.state[i][j] == 4:
                    return tuple([i, j])

    def is_movable(self, direction):    # test if field in direction of movement is empty or contains movable box

        test = (self.state[self.player_pos[0]+direction.x][self.player_pos[1]+direction.y] == 0
                or (self.state[self.player_pos[0]+direction.x][self.player_pos[1]+direction.y] == 2
                    and (self.state[self.player_pos[0]+2*direction.x][self.player_pos[1]+2*direction.y] == 0
                         or self.state[self.player_pos[0]+2*direction.x][self.player_pos[1]+2*direction.y] == 4)))\
               and not self.game_over()
        print("movable = %s" % test)
        return test

    def move(self, direction):
        if self.is_movable(direction):
            if self.state[self.player_pos[0]+direction.x][self.player_pos[1]+direction.y] == 2:
                self.state[self.player_pos[0] + 2 * direction.x][self.player_pos[1] + 2 * direction.y] = 2
            self.state[self.player_pos[0]][self.player_pos[1]] = 0
            self.state[self.player_pos[0] + direction.x][self.player_pos[1] + direction.y] = 3
            self.player_pos = tuple([self.player_pos[0]+direction.x, self.player_pos[1]+direction.y])
            if DEBUG:
                print("moved from %s to (%i, %i)" % self.player_pos, self.player_pos[0 + direction.x], self.player_pos[1 + direction.y])
        else:
            print("immovable!")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    F = Display()

    app.exec()
