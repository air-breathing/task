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
        self.data_about_polygon = [(1, 1), (5, 5), (1, 11)]

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
        rect = [(self.data_about_rect_start, (self.data_about_rect_start[0], self.data_about_rect_end[1])),
                ((self.data_about_rect_start[0], self.data_about_rect_end[1]), self.data_about_rect_end),
                (self.data_about_rect_end, (self.data_about_rect_end[0], self.data_about_rect_start[1])),
                ((self.data_about_rect_end[0], self.data_about_rect_start[1]), self.data_about_rect_start)]

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
                print(i, j)
                print(are_crossing((i[0][0], i[0][1], 0), (i[1][0], i[1][1], 0), (j[0][0], j[0][1], 0), ((j[1][0]), j[1][1], 0)))


def are_crossing(v11, v12, v21, v22):
    cut1 = difference(v12, v11)
    cut2 = difference(v22, v21)

    prod1 = cross(cut1 , difference(v21, v11))
    prod2 = cross(cut1, difference(v22, v11))

    if sign(prod1[2]) == sign(prod2[2]) or prod1[2] == 0 or prod2[2] == 0:
        return None

    prod1 = cross(cut2 , difference(v11, v21))
    prod2 = cross(cut2, difference(v12, v21))

    if sign(prod1[2]) == sign(prod2[2]) or prod1[2] == 0 or prod2[2] == 0:
        return None

    result = [0, 0]

    result[0] = v11[0] + cut1[0]*abs(prod1[2])/abs(prod2[2] - prod1[2])
    result[1] = v11[1] + cut1[1]*abs(prod1[2])/abs(prod2[2] - prod1[2])
    return result[0], result[1]


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
        return data

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