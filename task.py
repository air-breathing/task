#!/usr/bin/python3

from PyQt4 import QtGui, QtCore
import sys
import re


min_size_x = 300
min_size_y = 200
min_size_x_f = 150
min_size_y_f = 150
default_a = 1
default_b = 1
default_interval = (4, 10)

max_value_f = 100
min_value_f = -100
pattern = re.compile(r'\((.*?),(.*?)\)')

def f(a, b, x):
    if (x - a) * (x ** 2 + 2 * x) == 0:
        if (a * x ** 2 + b * x + 1) > 0:
            return max_value_f
        else:
            return min_value_f
    value = (a * x ** 2 + b * x + 1)/((x - a) * (x ** 2 + 2 * x))
    if min_value_f <= value and value <= max_value_f:
        return value
    if value > max_value_f:
        return max_value_f
    elif value < min_value_f:
        return min_value_f



class MyWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle('Задание по КГГ')
        self.setMinimumSize(min_size_x, min_size_y)
        frame = TaskScreen1(self)
        frame2 = TaskScreen2(self)
        frame3 = TaskScreen3(self)
        frame4 = TaskScreen4(self)
        frame5 = TaskScreen5(self)
        frame6 = TaskScreen6(self)
        tab = QtGui.QTabWidget()
        tab.addTab(frame, "&1 task")
        tab.addTab(frame2, "&2 task")
        tab.addTab(frame3, "&3 task")
        tab.addTab(frame4, "&4 task")
        tab.addTab(frame5, "&5 task")
        tab.addTab(frame6, "&6 task")
        self.setCentralWidget(tab)


class TaskScreen1(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.a_koef = 1
        self.b_koef = 1
        self.interval_a = -2
        self.interval_b = 10
        self.parent = parent
        self.box = QtGui.QHBoxLayout()
        self.boxLeft = QtGui.QVBoxLayout()
        self.boxRight = QtGui.QVBoxLayout()
        self.labelA = QtGui.QLabel(self)
        self.dataBox1 = 0
        self.dataBox2 = 0
        self.labelA.setText('Введите коэфициент a')
        #self.labelA.setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Raised)
        #self.labelA.setFixedHeight(40)
        self.button = QtGui.QPushButton('Перерисовать',self)
        self.connect(self.button, QtCore.SIGNAL('clicked()'), self.repaint)

        self.labelB = QtGui.QLabel(self)
        self.labelB.setText('Введите коэфициент b')
        self.labelInterval = QtGui.QLabel(self)
        self.labelInterval.setText('Введите отрезкок, на котором будем отображать')

        self.frame = Graphichs(self)
        self.boxRight.addWidget(self.frame)
        self.box.addLayout(self.boxLeft)
        self.box.addLayout(self.boxRight)
        self.dataBox1 = MyLineEdit(self, self.a_koef, 1)
        self.dataBox1.setFixedSize(100, 20)
        self.dataBox2 = MyLineEdit(self, self.b_koef, 2)
        self.dataBox3 = MyLineEdit(self, self.interval_a, 3)
        self.dataBox4 = MyLineEdit(self, self.interval_b, 4)
        self.dataBox2.setFixedSize(100, 20)
        self.dataBox3.setFixedSize(100, 20)
        self.dataBox4.setFixedSize(100, 20)
        self.labelA.setBuddy(self.dataBox1)
        self.labelB.setBuddy(self.dataBox2)
        self.labelInterval.setBuddy(self.dataBox3)
        self.labelInterval.setBuddy(self.dataBox4)
        self.boxLeft.addWidget(self.labelA)
        self.boxLeft.addWidget(self.dataBox1)
        self.boxLeft.addWidget(self.labelB)
        self.boxLeft.addWidget(self.dataBox2)
        self.boxLeft.addWidget(self.labelInterval)
        self.boxLeft.addWidget(self.dataBox3)
        self.boxLeft.addWidget(self.dataBox4)
        self.boxLeft.addWidget(self.button)
        self.setLayout(self.box)

class MyLineEdit(QtGui.QLineEdit):
    def __init__(self, parent, data, num):
        QtGui.QLineEdit.__init__(self)
        self.num = num
        self.parent = parent
        parent.connect(self, QtCore.SIGNAL('editingFinished()'), self._change)
        self.setText(str(data))

    def _change(self):
        if self.num == 1:
            self.parent.a_koef = int(self.text())
        elif self.num == 2:
            self.parent.b_koef = int(self.text())
        elif self.num == 3:
            self.parent.interval_a = int(self.text())
        else:
            self.parent.interval_b = int(self.text())

class Graphichs(QtGui.QFrame):
    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)
        self.setStyleSheet('border: 1px solid black')
        self.parent = parent
        self.setMinimumSize(min_size_x_f, min_size_y_f)

    def repaint(self):
        self.paintEvent(None)

    def paintEvent(self, event):
        self.standart_x = 150
        self.standart_y = 150
        self._drawGraphic(self.parent.a_koef, self.parent.b_koef, (self.parent.interval_a, self.parent.interval_b),
                          self.size())


    def _drawGraphic(self, a, b, interval, size):
        painter = QtGui.QPainter(self)
        self.maxy = size.height()
        self.maxx = size.width()
        self.dx = self.maxx/self.standart_x
        self.dy = self.maxy/self.standart_y
        self.standart_x = self.maxx
        self.standart_y = self.maxy
        self.ymin = self.ymax = f(a, b, interval[0])
        if self.ymin is None:
            self.ymin = 0
            self.ymax = 0
        for xx in range(self.maxx):
            x = interval[0] + xx * (interval[1] - interval[0])/self.maxx
            y = f(a, b, x)
            if y is None:
                pass
            else:
                if y < self.ymin:
                    self.ymin = y
                if y > self.ymax:
                    self.ymax = y
        # print(self.ymax, self.ymin)
        f_a = f(a, b, interval[0])
        if f_a is not None:
            if self.ymax - self.ymin > 0:
                yy = (f_a - self.ymin)*self.maxy/(self.ymax - self.ymin)
            else:
                if (f_a - self.ymin)*self.maxy > 0:
                    yy = -100
                elif (f_a - self.ymin)*self.maxy == 0:
                    yy = 0
                else:
                    yy = 100
            painter.drawPoint(0, yy)
        for xx in range(self.maxx):
            x = interval[0] + xx * (interval[1] - interval[0])/self.maxx
            y = f(a, b, x)
            if y is not None:
                # yy = (y - self.ymax) * self.maxy/(self.ymin - self.ymax)*self.dy/self.dx
                if self.ymax - self.ymin > 0:
                    yy = (y - self.ymax) * self.maxy/(self.ymin - self.ymax)
                else:
                    if (f_a - self.ymin)*self.maxy > 0:
                        yy = -100
                    elif (f_a - self.ymin)*self.maxy == 0:
                        yy = 0
                    else:
                        yy = 100
                painter.drawPoint(xx, yy)


class TaskScreen2(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.x0 = 0
        self.y0 = 0
        self.x1 = 100
        self.y1 = 100
        self.box = QtGui.QHBoxLayout()
        self.boxLeft = QtGui.QVBoxLayout()
        self.boxRight = QtGui.QVBoxLayout()
        self.labelA = QtGui.QLabel(self)
        self.dataBox1 = 0
        self.dataBox2 = 0
        self.labelA.setText('Введите точку x1')
        self.button = QtGui.QPushButton('Перерисовать',self)
        self.connect(self.button, QtCore.SIGNAL('clicked()'), self.repaint)
        self.labelB = QtGui.QLabel(self)
        self.labelB.setText('Введите точку x2')
        self.labelInterval = QtGui.QLabel(self)
        self.labelInterval.setText('Введите отрезкок, на котором будем отображать')
        self.frame = Graphichs2(self)
        self.boxRight.addWidget(self.frame)
        self.box.addLayout(self.boxLeft)
        self.box.addLayout(self.boxRight)
        self.dataBox1 = MyLineEdit2(self, self.x1, 1)
        self.dataBox1.setFixedSize(100, 20)
        self.dataBox2 = MyLineEdit2(self, self.y1, 2)
        self.dataBox2.setFixedSize(100, 20)
        self.labelA.setBuddy(self.dataBox1)
        self.labelB.setBuddy(self.dataBox2)
        self.boxLeft.addWidget(self.labelA)
        self.boxLeft.addWidget(self.dataBox1)
        self.boxLeft.addWidget(self.labelB)
        self.boxLeft.addWidget(self.dataBox2)
        self.boxLeft.addWidget(self.labelInterval)
        self.boxLeft.addWidget(self.button)
        self.setLayout(self.box)

class Graphichs2(QtGui.QFrame):
    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)
        self.setStyleSheet('border: 1px solid black')
        self.parent = parent
        self.setMinimumSize(min_size_x_f, min_size_y_f)

    def repaint(self):
        self.paintEvent(None)

    def paintEvent(self, event):
        dx = abs(self.parent.x1 - self.parent.x0)
        dy = abs(self.parent.y1 - self.parent.y0)
        s1 = -1*sign(self.parent.x1 - self.parent.x0)
        s2 = -1*sign(self.parent.y1 - self.parent.y0)
        x = self.parent.x0
        y = self.parent.y0
        change = 0
        if dy > dx:
            temp = dx
            dx = dy
            dy = temp
            change = 1
        e = 2 * dy - dx
        painter = QtGui.QPainter(self)
        for i in range(dx):
            # print(x, y)
            painter.drawPoint(x, y)
            while (e >= 0):
                if change == 1:
                    x += s1
                else:
                    y += s2
                e -= 2 * dx
            if change == 1:
                y += s2
            else:
                x += s1
            e += 2 * dy

def sign(data):
    if data > 0:
        return -1
    elif data < 0:
        return 1
    else:
        return 0

class MyLineEdit2(QtGui.QLineEdit):
    def __init__(self, parent, data, num):
        QtGui.QLineEdit.__init__(self)
        self.num = num
        self.parent = parent
        parent.connect(self, QtCore.SIGNAL('editingFinished()'), self._change)
        self.setText(str(data))

    def _change(self):
        if self.num == 1:
            self.parent.x1 = int(self.text())
        elif self.num == 2:
            self.parent.y1 = int(self.text())


class TaskScreen3(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.x0 = 0
        self.y0 = 0
        self.x1 = 100
        self.y1 = 100
        self.p = 1
        self.box = QtGui.QHBoxLayout()
        self.boxLeft = QtGui.QVBoxLayout()
        self.boxRight = QtGui.QVBoxLayout()
        self.labelA = QtGui.QLabel(self)
        self.dataBox1 = 1
        self.labelA.setText('Введите точку P')
        self.button = QtGui.QPushButton('Перерисовать',self)
        self.connect(self.button, QtCore.SIGNAL('clicked()'), self.repaint)
        self.frame = Graphichs3(self)
        self.boxRight.addWidget(self.frame)
        self.box.addLayout(self.boxLeft)
        self.box.addLayout(self.boxRight)
        self.dataBox1 = MyLineEdit3(self, self.p, 1)
        self.dataBox1.setFixedSize(100, 20)
        self.labelA.setBuddy(self.dataBox1)
        self.boxLeft.addWidget(self.labelA)
        self.boxLeft.addWidget(self.dataBox1)
        self.boxLeft.addWidget(self.button)
        self.setLayout(self.box)

class Graphichs3(QtGui.QFrame):
    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)
        self.setStyleSheet('border: 1px solid black')
        self.parent = parent
        self.setMinimumSize(min_size_x_f, min_size_y_f)

    def repaint(self):
        self.paintEvent(None)

    def paintEvent(self, event):
        p = self.parent.p
        painter = QtGui.QPainter(self)
        height = self.height()
        half_height = self.height()/2
        width = self.width()
        x = 0
        y = 0
        i = 0
        while i < width:
            s_l = y ** 2 - 2 * p * (x + 1)
            s_h = (y + 1) ** 2 - 2 * p * x
            s_v = (y + 1) ** 2 - 2 * p * (x + 1)
            painter.drawPoint(x, - y + half_height)
            painter.drawPoint(x, y + half_height)
            if s_v < 0:
                if abs(s_v) - abs(s_h) <= 0:
                    x += 1
                    y += 1
                else:
                    y += 1
            else:
                if abs(s_v) - abs(s_l) <= 0:
                    x += 1
                    y += 1
                else:
                    x += 1
            i += 1


def sign(data):
    if data > 0:
        return -1
    elif data < 0:
        return 1
    else:
        return 0


class MyLineEdit3(QtGui.QLineEdit):
    def __init__(self, parent, data, num):
        QtGui.QLineEdit.__init__(self)
        self.num = num
        self.parent = parent
        parent.connect(self, QtCore.SIGNAL('editingFinished()'), self._change)
        self.setText(str(data))

    def _change(self):
        self.parent.p = int(self.text())


class TaskScreen4(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.data_about_rect_start = (0, 0)
        self.data_about_rect_end = (10, 10)
        # self.data_about_polygon = [(1, 1), (1, 11), (5, 5)]
        # self.data_about_polygon = [(10, 10), (10, 11), (11, 10)]
        # self.data_about_polygon = [(10, 0), (8, 0), (11, 6)]
        # self.data_about_polygon = [(9, -6), (8, 0), (11, 6)]
        self.data_about_polygon = [(5, -5), (-3, 3), (13, 3)]


        self.parent = parent
        self.box = QtGui.QHBoxLayout()
        self.boxLeft = QtGui.QVBoxLayout()
        self.boxRight = QtGui.QVBoxLayout()

        self.labelA = QtGui.QLabel(self)
        self.labelA.setText('В формате точки(10, 10) укажите левый нижний угол прямоугольника')

        self.labelB = QtGui.QLabel(self)
        self.labelB.setText('В формате точка (10, 10) укажите правый верхний угол прямоугольника')

        self.labelC = QtGui.QLabel(self)
        self.labelC.setText('В формате (10, 10), (10, 10), по часовой стрелки перечислите все углы многоугольника')

        self.button = QtGui.QPushButton('Пересчитать', self)
        self.connect(self.button, QtCore.SIGNAL('clicked()'), self.recount)

        self.box.addLayout(self.boxLeft)
        self.box.addLayout(self.boxRight)

        self.dataBox1 = MyLineEdit4(self, self.data_about_rect_start, 1)
        self.dataBox1.setFixedSize(200, 20)

        self.dataBox2 = MyLineEdit4(self, self.data_about_rect_end, 2)
        self.dataBox2.setFixedSize(200, 40)

        self.dataBox3 = MyLineEdit4(self, self.data_about_polygon, 3)
        self.dataBox3.setMaximumSize(200, 40)

        self.labelA.setBuddy(self.dataBox1)
        self.labelB.setBuddy(self.dataBox2)
        self.labelC.setBuddy(self.dataBox3)
        self.boxLeft.addWidget(self.labelA)
        self.boxLeft.addWidget(self.dataBox1)
        self.boxLeft.addWidget(self.labelB)
        self.boxLeft.addWidget(self.dataBox2)
        self.boxLeft.addWidget(self.labelC)
        self.boxLeft.addWidget(self.dataBox3)
        self.boxLeft.addWidget(self.button)
        self.setLayout(self.box)

    def recount(self):
        segments = []
        points_of_interection = []
        angle_points = []
        #rect = [(self.data_about_rect_start, (self.data_about_rect_start[0], self.data_about_rect_end[1])),
        #        ((self.data_about_rect_start[0], self.data_about_rect_end[1]), self.data_about_rect_end),
        #        (self.data_about_rect_end, (self.data_about_rect_end[0], self.data_about_rect_start[1])),
        #        ((self.data_about_rect_end[0], self.data_about_rect_start[1]), self.data_about_rect_start)]
        rect = [(self.data_about_rect_start, (self.data_about_rect_end[1], self.data_about_rect_start[0])),
                ((self.data_about_rect_end[1], self.data_about_rect_start[0]), self.data_about_rect_end),
                (self.data_about_rect_end, (self.data_about_rect_start[1], self.data_about_rect_end[0])),
                ((self.data_about_rect_start[1], self.data_about_rect_end[0]), self.data_about_rect_start)]
        rect_angles = [self.data_about_rect_start, (self.data_about_rect_start[0], self.data_about_rect_end[1]),
                       self.data_about_rect_end,   (self.data_about_rect_end[0], self.data_about_rect_start[1])]

        for i in range(len(self.data_about_polygon)):
            if i + 1 == len(self.data_about_polygon):
                j = 0
            else:
                j = i + 1
            segments.append((
                (self.data_about_polygon[i][0], self.data_about_polygon[i][1]),
                (self.data_about_polygon[j][0], self.data_about_polygon[j][1])))
        for i in rect:
            for j in segments:
                res = are_crossing((i[0][0], i[0][1], 0), (i[1][0], i[1][1], 0),
                                   (j[0][0], j[0][1], 0), ((j[1][0]), j[1][1], 0))
                if res:
                    print(res, 'res')
                    points_of_interection.append(res)
        if points_of_interection:
            all_points = add_points(self.data_about_polygon, points_of_interection, rect_angles)
            print(all_points, 'all_points')
            # res = intersection(points_of_interection, all_points, rect_angles, self.data_about_polygon)
            on_points = getOnPoints(all_points, rect_angles)
            out_points = getOutPoints(all_points, rect_angles)
            print(on_points, 'on_point')
            print(out_points, 'out_point')
            res = searchInterection(all_points, on_points, out_points)
            print(res)
        else:
            print('не пересекается')

def searchInterection(all_points, on_points, out_points):
    used_points = []

    return  all_points

def getOnPoints(points, rect_angles):
    res = []
    for point in points:
        print(point[0])
        if check_on_rect(point[0], rect_angles):
           res.append(point)
    return res

def getOutPoints(points, rect_angles):
    res = []
    for point in points:
        print(point[0])
        if check_out_rect(point[0], rect_angles):
           res.append(point)
    return res


def add_points(polygon, points_of_interscert, angles):
    result = []
    prev = polygon[-1]
    data = {}
    #print(points_of_interscert, 'points of interection')
    for elem in points_of_interscert:
        s = data.get((elem[1], elem[2]), set())
        if s:
            s.add((elem[0], (elem[1], elem[2]) ,(elem[3], elem[4])))
            data[(elem[1], elem[2])] = s
        else:
            s = data.get((elem[2], elem[1]), set())
            s.add((elem[0], (elem[1], elem[2]),(elem[3], elem[4])))
            data[(elem[2], elem[1])] = s
    # сортировка
    for k in data.keys():
        new_order = sorted(data[k], key=lambda x: x[0][0]**2 + x[0][1]**2)
        data[k] = new_order
    #print(data, 'data')
    for elem in polygon:
        #print(result, 'промежуточный результат добавления')
        #print(elem, 'текущий угол многоугольника')
        result.append((prev, ))
        s0 = data.get((prev, elem), None)
        s1 = data.get((elem, prev), None)
        if s0:
            s = s0
        else:
            s = s1
        if s:
            for i in s:
                last = result[-1]
                if i != last:
                    #print(i, 'добавление еще элемента')
                    result.append(i)
        prev = elem
    return result


def compare(i, j):
    print(i,'i')
    print(j, 'j')
    if (len(i) == len(j)):
        if (i[0] == j[0] and i[1][0] == j[1][0] and i[1][1] == j[1][1] and
                    i[2][0] == j[2][0] and i[2][1] == j[2][1]):
            return True
    return False



def intersection(points, all_points, rect_angles, polygon):
    print(points)
    print(all_points)
    print(rect_angles)
    print(polygon)
    start_search = None
    used_out_points = []
    result = []
    out_points = []
    in_points = []
    on_points = []
    angle_points = []
    angles = [rect_angles[0], rect_angles[3], rect_angles[2], rect_angles[1]]
    # выделяем все внешние точки
    for point in all_points:
        if check_in_rect(point, rect_angles):
            in_points.append(point)
        if check_out_rect(point, rect_angles):
            out_points.append(point)
        if check_on_rect(point, rect_angles):
            on_points.append(point)
        if check_angle(point, rect_angles):
            angle_points.append(point)
    print(in_points)
    print(out_points)
    print(on_points)
    on_points = list(set(on_points))
    on_points = orderOnPoints(on_points, angles)
    print(on_points, 'упорядоченные по часовой внешние точки')

    i = 10
    while len(used_out_points) < len(out_points) and i > 0:
        circle = []
        i -= 1
        # ищем первую точку вне прямоугольника не использованную
        start_search = None
        for i in range(len(out_points)):
            # если данная точка не использована при поиске
            if not out_points in used_out_points:
                start_search = all_points.index(out_points[i])
                used_out_points.append(out_points[i])
                circle.append(out_points[i])
                break
        if start_search is None:
            return result
        q1 = 0
        current_i = (start_search + 1) % len(all_points)
        prev_i = start_search
        wait_last_on = False
        last_on = None
        while q1 > 0:
            # пока идем по внешним точкам
            # print(all_points[current_i], current_i, wait_last_on)
            if all_points[current_i] in out_points:
                if all_points[current_i] in out_points:
                    pass
                if all_points[current_i] in on_points:
                    if all_points[current_i] in angle_points:
                        pass
                    else:
                        pass
            q1 -= 1
            prev_i = current_i
            current_i = (current_i + 1) % len(all_points)
        result.append(circle)
    return result

def orderOnPoints(on_points, angles):
    left = []
    right = []
    bottom = []
    above = []
    was_add = False
    for point in on_points:
        was_add = False
        # на верхней
        if angles[0][0] == point[0] and not was_add:
            left.append(point)
            was_add = True
        if angles[2][0] == point[0] and not was_add:
            right.append(point)
            was_add = True
        if angles[0][1] == point[1] and not was_add:
            above.append(point)
            was_add = True
        if angles[1][0] == point[1] and not was_add:
            bottom.append(point)
            was_add = True
    result = []
    left = sorted(left, key=lambda x: x[1], reverse=True)
    bottom = sorted(bottom, key=lambda x: x[0], reverse=True)
    right = sorted(right, key=lambda x: x[1])
    above = sorted(above, key=lambda x: x[0])
    print(left, bottom, right, above, sep='упорядоченность\n')
    result.extend(above)
    result.extend(right)
    result.extend(bottom)
    result.extend(left)
    return result


def check_in_rect(point, rect_angles):
    if rect_angles[0][0] < point[0] and point[0] < rect_angles[2][0]:
        if rect_angles[0][1] < point[1] and point[1] < rect_angles[1][1]:
            return True
    return False

def getSide(rect_angles, point):
    if rect_angles[0][0] == point[0]:
        return (rect_angles[1], rect_angles[0])
    elif rect_angles[0][1] == point[1]:
        return (rect_angles[0], rect_angles[3])
    elif rect_angles[2][0] == point[0]:
        return (rect_angles[3], rect_angles[2])
    elif rect_angles[2][1] == point[1]:
        return (rect_angles[2], rect_angles[1])
    else:
        print('error in getSide')

def check_out_rect(point, rect_angles):
    if rect_angles[0][0] <= point[0] and point[0] <= rect_angles[2][0]:
        if rect_angles[0][1] <= point[1] and point[1] <= rect_angles[1][1]:
            return False
    return True


def check_on_rect(point, rect_angles):
    if rect_angles[0][0] <= point[0] and point[0] <= rect_angles[2][0]:
        if rect_angles[0][1] == point[1] or point[1] == rect_angles[1][1]:
            return True
    if rect_angles[0][1] <= point[1] and point[1] <= rect_angles[1][1]:
        if rect_angles[0][0] == point[0] or point[0] == rect_angles[2][0]:
            return True
    return False

def check_angle(point, rect_angles):
    if rect_angles[0][0] == point[0] or point[0] == rect_angles[2][0]:
        if rect_angles[0][1] == point[1] or point[1] == rect_angles[1][1]:
            return True
    return False


def are_crossing(v11, v12, v21, v22):
    cut1 = difference(v12, v11)
    cut2 = difference(v22, v21)

    prod1 = cross(cut1, difference(v21, v11))
    prod2 = cross(cut1, difference(v22, v11))

    if sign(prod1[2]) == sign(prod2[2]):
            #or prod1[2] == 0 or prod2[2] == 0:
        return None

    prod1 = cross(cut2 , difference(v11, v21))
    prod2 = cross(cut2, difference(v12, v21))

    if sign(prod1[2]) == sign(prod2[2]):
            #or prod1[2] == 0 or prod2[2] == 0:
        return None

    result = [0, 0]

    result[0] = (v11[0]*abs(prod2[2] - prod1[2]) + cut1[0]*abs(prod1[2]))/abs(prod2[2] - prod1[2])
    result[1] = (v11[1]*abs(prod2[2] - prod1[2]) + cut1[1]*abs(prod1[2]))/abs(prod2[2] - prod1[2])
    return [(result[0], result[1]), (v21[0],v21[1]), (v22[0],v22[1]), (v11[0],v11[1]), (v12[0],v12[1])]


def cross(v1, v2):
    return v1[1]*v2[2] - v1[2]*v2[1], v1[0]*v2[2] - v1[2]*v2[0], v1[0]*v2[1] - v1[1]*v2[0]


def difference(v1, v2):
    return v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2]


class MyLineEdit4(QtGui.QLineEdit):
    def __init__(self, parent, data, num):
        QtGui.QLineEdit.__init__(self)
        self.num = num
        self.parent = parent
        parent.connect(self, QtCore.SIGNAL('editingFinished()'), self._change)
        self.setText(str(data))

    def _change(self):
        if self.num == 1:
            # информация о левой нижней координате
            self.parent.data_about_rect_start = self._parseRect(self.text())
        elif self.num == 2:
            # информация о правой верхней координате
            self.parent.data_about_rect_end = self._parseRect(self.text())
        elif self.num == 3:
            self.parent.data_about_polygon = self._parseCoord(self.text())

    def _parseCoord(self, text):
        data = pattern.findall(text)
        data = map(lambda x: (int(x[0]), int(x[1])), data)
        return list(data)

    def _parseRect(self, text):
        data = pattern.findall(text)
        return int(data[0][0]), int(data[0][1])


class TaskScreen5(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)


class TaskScreen6(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)


def main():
    app = QtGui.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
