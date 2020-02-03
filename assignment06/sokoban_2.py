import sys

# import enum
from dataclasses import dataclass

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import heapq

WIDTH = 250
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
            else:
                self.games[0].move(Directions.east)
                self.games[0].refresh_widget(True)
        self.widget.update()

        if event.key() == Qt.Key_F:
            # self.dfs()
            # for map in self.games:
            #     print(map.is_possible())
            print(self.games[1].is_possible())
            #TODO: is_possible funzt soweit für alle sokban instanzen. nur map1 wird nich als lösbar erkannt

        def dfs(self, n=2):
            q = []
            visited = dict()

            players, boxes, targets, fields = self.getStats(n)
            d = []
            tupl = tuple()

            for i in range(n):
                d.append(self.dist(boxes[i][0], boxes[i][1], targets[i][0], targets[i][1]) +
                         self.dist(players[i][0], players[i][1],
                                   boxes[i][0], boxes[i][1]))
                tupl += (players[i][0], players[i][1], boxes[i][0], boxes[i][1])

            d = max(d)

            start = self.Node(d, 0, tupl)
            q.append(start)
            heapq.heapify(q)
            count = 0

            # Solange noch Wege möglich sind, werden sie exploriert, dabei wird immer
            # der Zug mit dem kleinsten Wert genommen, da Priority-Queue.
            while q:
                count += 1
                node = heapq.heappop(q)
                visited[node.state] = True

                up = tuple()
                down = tuple()
                left = tuple()
                right = tuple()

                upc = downc = leftc = rightc = 0

                finished = [0 for _ in range(n)]

                for i in range(n):
                    if sum(finished) == n:
                        print("Iterationen:", count)
                        print("Weglänge:", node.count)
                        print("MD vom Anfang:", d)
                        self.printWay(node)
                        return True

                    xP = node.state[0 + 4 * i]
                    yP = node.state[1 + 4 * i]
                    xB = node.state[2 + 4 * i]
                    yB = node.state[3 + 4 * i]

                    # Ist das Ende erreicht, soll der Pfad ausgegeben werden
                    if (xB, yB) == targets[i]:
                        finished[i] = 1
                        up += node.state
                        down += node.state
                        left += node.state
                        right += node.state
                        upc = downc = leftc = rightc = 0
                        continue

                    # Klassische Tiefensuche nach Dijkstra, es werden alle möglichen Züge
                    # durchprobiert unter Bedacht der Heuristiken und je nachdem, ob sie
                    # möglich sind, noch nicht besucht sind und nicht zu einen Deadlock
                    # führen.
                    _up, up_count = self.moveUp(
                        xP, yP, xB, yB, targets[i], fields[i], node.count)
                    _down, down_count = self.moveDown(
                        xP, yP, xB, yB, targets[i], fields[i], node.count)
                    _left, left_count = self.moveLeft(
                        xP, yP, xB, yB, targets[i], fields[i], node.count)
                    _right, right_count = self.moveRight(
                        xP, yP, xB, yB, targets[i], fields[i], node.count)

                    up += _up
                    down += _down
                    left += _left
                    right += _right

                    upc = up_count if upc > up_count else upc
                    downc = down_count if down_count > downc else downc
                    leftc = left_count if left_count > leftc else leftc
                    rightc = right_count if right_count > rightc else rightc

                def check_all():
                    end = True
                    for i in range(n):
                        end = end and Game.is_possible(
                            node.state[2 + 4 * i], node.state[3 + 4 * i], targets[i], fields[i])
                    return end

                # TODO: write function to check all fields
                if not up in visited and check_all():
                    up = self.Node(upc, node.count + 1, up)
                    up.parent = node
                    visited[up.state] = True
                    heapq.heappush(q, up)
                if not down in visited and check_all():
                    down = self.Node(downc, node.count + 1, down)
                    down.parent = node
                    visited[down.state] = True
                    heapq.heappush(q, down)
                if not left in visited and check_all():
                    left = self.Node(leftc, node.count + 1, left)
                    left.parent = node
                    visited[left.state] = True
                    heapq.heappush(q, left)
                if not right in visited and check_all():
                    right = self.Node(rightc, node.count + 1, right)
                    right.parent = node
                    visited[right.state] = True
                    heapq.heappush(q, right)

                if sum(finished) == n:
                    print("Iterationen:", count)
                    print("Weglänge:", node.count)
                    print("MD vom Anfang:", d)
                    self.printWay(node)
                    return True

            # Das sollte eigentlich nie erreicht werden
            print(count)
            print("no way found")
            return None


class Sokoban:

    def __init__(self, map):
        self.state = map
        self.game_size = len(self.state[0])  # all maps must be squares an have the same size!
        self.player_pos = self.get_pos(3)
        self.box_pos = self.get_pos(2)
        self.destination = self.get_pos(4)
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
                player_pos = self.get_pos(3)
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

    def get_pos(self, target):   # set target 3 for player, 2 for box, 4 for destination
        for i in range(self.game_size):
            for j in range(self.game_size):
                if self.state[i][j] == target:
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
                self.box_pos = tuple([self.box_pos[0]+direction.x, self.box_pos[1]+direction.y])
            self.state[self.player_pos[0]][self.player_pos[1]] = 0
            self.state[self.player_pos[0] + direction.x][self.player_pos[1] + direction.y] = 3
            self.player_pos = tuple([self.player_pos[0]+direction.x, self.player_pos[1]+direction.y])
            if DEBUG:
                print("moved from %s to (%i, %i)" % self.player_pos, self.player_pos[0 + direction.x], self.player_pos[1 + direction.y])
        else:
            print("immovable!")

    def is_possible(self):
        x, y = self.box_pos[0], self.box_pos[1]
        target = tuple([self.destination[0], self.destination[1]])

        # False on win
        if (x, y) == target:
            return True

        # False if box is in a corner
        if y - 1 >= 0:
            if self.state[x][y - 1] == 1:
                if x + 1 < self.game_size and x - 1 >= 0:
                    if self.state[x + 1][y] == 1 or self.state[x - 1][y] == 1:
                        return False
        if y + 1 < self.game_size:
            if self.state[x][y + 1] == 1:
                if x + 1 < self.game_size and x - 1 >= 0:
                    if self.state[x + 1][y] == 1 or self.state[x - 1][y] == 1:
                        return False

        # True if box is in a tunnel
        if (self.state[x - 1][y] == self.state[x + 1][y] and self.state[x - 1][y] == 1) \
                or (self.state[x][y - 1] == self.state[x][y + 1] and self.state[x][y + 1] == 1):
            return True

        # False if box is at a wall and cannot be moved away
        if self.state[x][y - 1] == 1:
            if sum(row[y - 1] for row in self.state) > self.game_size - 1:
                return False
        if self.state[x][y + 1] == 1:
            if sum(row[y + 1] for row in self.state) > self.game_size - 1:
                return False
        if self.state[x - 1][y] == 1:
            if sum(self.state[x:, - 1]) > self.game_size - 1:
                return False
        if self.state[x + 1][y] == 1:
            if sum(self.state[:, x + 1]) > self.game_size - 1:
                return False

        # False if box is at outer wall and target is not on that side
        if y == 1:
            if target[1] != 0:
                return False
        if y == self.game_size - 2:
            if target[1] != self.game_size - 1:
                return False
        if x == 1:
            if target[0] != 0:
                return False
        if x == self.game_size - 2:
            if target[0] != self.game_size - 1:
                return False

        return True

if __name__ == '__main__':
    app = QApplication(sys.argv)

    F = Display()

    app.exec()
