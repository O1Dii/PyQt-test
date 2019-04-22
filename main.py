import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import random
import math


class MyWindow(QMainWindow):
    window_height = 600
    window_width = 600

    def __init__(self):
        super(QWidget, self).__init__()
        self.setGeometry(100, 100, self.window_height, self.window_width)

        oImage = QImage("background.png")
        sImage = oImage.scaled(QSize(self.window_height, self.window_width))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

    def initUI(self):
        self.setGeometry(750, 450, 200, 200)
        self.setWindowTitle('Points')
        self.show()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        qp.end()

    def drawPoints(self, qp):
        global points
        for x, y, _, _, _, _, _, _ in points:
            for x1, y1, _, _, _, _, _, _ in points:
                a = math.sqrt(abs(x1 - x) ** 2 + abs(y1 - y) ** 2)
                if 255 > a > 1:
                    pen = QPen(QColor(255, 100, 0, (5000 / a)), 3, Qt.SolidLine)
                    qp.setPen(pen)
                    qp.drawLine(x, y, x1, y1)
                x1 = x
                y1 = y
                pen = QPen(QColor(100, 200, 200, 200), 4, Qt.SolidLine)
                qp.setPen(pen)
                qp.drawEllipse(x1 - 3, y1 - 3, 6, 6)


class Dot:
    x = 0
    y = 0
    dest_x = 0
    dest_y = 0


def updateValues():
    global points, acceleration
    for i in range(len(points)):
        if points[i][4] is True:
            if points[i][0] < points[i][2]:
                points[i][6] *= acceleration
                points[i][0] += points[i][6]
            else:
                points[i][6] *= 1/acceleration
                points[i][0] += points[i][6]
        else:
            if points[i][0] > points[i][2]:
                points[i][6] *= acceleration
                points[i][0] -= points[i][6]
            else:
                points[i][6] *= 1/acceleration
                points[i][0] -= points[i][6]
        if points[i][5] is True:
            if points[i][1] < points[i][3]:
                points[i][7] *= acceleration
                points[i][1] += points[i][7]
            else:
                points[i][7] *= 1/acceleration
                points[i][1] += points[i][7]
        else:
            if points[i][1] > points[i][3]:
                points[i][7] *= acceleration
                points[i][1] -= points[i][7]
            else:
                points[i][7] *= 1/acceleration
                points[i][1] -= points[i][7]
        if points[i][0] < 0:
            points[i][0] = 0
        elif points[i][0] > 500:
            points[i][0] = 500
        if points[i][1] < 0:
            points[i][1] = 0
        elif points[i][1] > 500:
            points[i][1] = 500
        print(points)
    mw.update()  # <-- update the window!


def updateSpeed():
    global points, speed_x, speed_y
    for i in range(len(points)):
        rand_dot = random.randint(100, 400)
        points[i][2] = (points[i][0] + rand_dot) / 2
        rand_dot = random.randint(100, 400)
        points[i][3] = (points[i][1] + rand_dot) / 2
        points[i][4] = False
        points[i][5] = False
        points[i][6] = speed_x
        points[i][7] = speed_y
        if points[i][0] < points[i][2]:
            points[i][4] = True
        if points[i][1] < points[i][3]:
            points[i][5] = True
    mw.update()


middle_x = 0
middle_y = 0
direction_x_pos = False
direction_y_pos = False
time_speed = 2000
speed_x = 500/time_speed
speed_y = 500/time_speed
acceleration = (math.sqrt(time_speed)*2)/(math.sqrt(500)*3)


app = QApplication(sys.argv)

amount = int(input('Введите количество точек: '))
points = list()
for i in range(amount):
    dot = Dot()
    dot.x = random.randint(0, 500)
    dot.y = random.randint(0, 500)
    dot.dest_x = random.randint(0, 500)
    dot.dest_y = random.randint(0, 500)
    middle_x = (dot.x + dot.dest_x) / 2
    middle_y = (dot.y + dot.dest_y) / 2
    if dot.x < middle_x:
        direction_x_pos = True
    if dot.y < middle_y:
        direction_y_pos = True
    xy = [dot.x, dot.y, middle_x, middle_y, direction_x_pos, direction_y_pos, speed_x, speed_y]
    points.append(xy)
print(points)

mw = MyWindow()
mw.setWindowTitle('PyQt5 - Main Window')
mw.setWindowIcon(QIcon("icon.jpg"))

timer = QTimer()
timer1 = QTimer()
timer1.timeout.connect(updateSpeed)
timer1.start(time_speed)
timer.timeout.connect(updateValues)
timer.start(20)

mw.show()
sys.exit(app.exec_())
