import copy
import time
import sys
import json
import glob
import time
import random
import numpy as np


from IK import *

try:
    from PyQt5 import QtCore
    from PyQt5.QtCore import pyqtSlot
    from PyQt5 import QtWidgets, QtGui
    from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox
    from PyQt5.QtWidgets import *
    from PyQt5.uic import loadUi
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
except Exception as e:
    print("Requirement Error! The PyQt Libs are not installed.")
    import os
import math
import matplotlib.pyplot as plt


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        try:
            loadUi('test.ui', self)
        except Exception as e:
            print(e)
            print("main.ui could not be found!")

        self.radius = 20
        self.coxaLength = 60
        self.tibiaLength = 120
        self.femurLength = 80

        self.translateX = 0
        self.translateY = 0
        self.translateZ = 0

        self.rotX = 0
        self.rotY = 0
        self.rotZ = 0

        self.trace = self.radioButton.isChecked()
        self.trajectory = False

        self.xPoint = [85, 85, 85, 85]
        self.yPoint = [100, 100, 100, 100]
        self.zPoint = [0, 0, 0, 0]

        self.pushButton_4.clicked.connect(lambda: self.handleIncrement("x"))
        self.pushButton_6.clicked.connect(lambda: self.handleIncrement("y"))
        self.pushButton_9.clicked.connect(lambda: self.handleIncrement("z"))

        self.pushButton_5.clicked.connect(lambda: self.handleDecrement("x"))
        self.pushButton_7.clicked.connect(lambda: self.handleDecrement("y"))
        self.pushButton_8.clicked.connect(lambda: self.handleDecrement("z"))

        self.setXTranslate(self.translateX)
        self.setYTranslate(self.translateY)
        self.setZTranslate(self.translateZ)

        self.setXRotate(self.rotX)
        self.setYRotate(self.rotY)
        self.setZRotate(self.rotZ)

        # self.horizontalSlider.valueChanged.connect(self.movePointX)
        # self.horizontalSlider_2.valueChanged.connect(self.movePointY)
        # self.horizontalSlider_3.valueChanged.connect(self.movePointZ)

        #Leg - 1
        self.horizontalSlider.valueChanged.connect(
            lambda value, point="x", leg=1: self.moveLeg(value, point, leg))
        self.horizontalSlider_2.valueChanged.connect(
            lambda value, point="y", leg=1: self.moveLeg(value, point, leg))
        self.horizontalSlider_3.valueChanged.connect(
            lambda value, point="z", leg=1: self.moveLeg(value, point, leg))

        #Leg - 2
        self.horizontalSlider_18.valueChanged.connect(
            lambda value, point="x", leg=2: self.moveLeg(value, point, leg))
        self.horizontalSlider_16.valueChanged.connect(
            lambda value, point="y", leg=2: self.moveLeg(value, point, leg))
        self.horizontalSlider_17.valueChanged.connect(
            lambda value, point="z", leg=2: self.moveLeg(value, point, leg))

        #Leg - 3
        self.horizontalSlider_15.valueChanged.connect(
            lambda value, point="x", leg=3: self.moveLeg(value, point, leg))
        self.horizontalSlider_13.valueChanged.connect(
            lambda value, point="y", leg=3: self.moveLeg(value, point, leg))
        self.horizontalSlider_14.valueChanged.connect(
            lambda value, point="z", leg=3: self.moveLeg(value, point, leg))

        #Leg - 4
        self.horizontalSlider_21.valueChanged.connect(
            lambda value, point="x", leg=4: self.moveLeg(value, point, leg))
        self.horizontalSlider_19.valueChanged.connect(
            lambda value, point="y", leg=4: self.moveLeg(value, point, leg))
        self.horizontalSlider_20.valueChanged.connect(
            lambda value, point="z", leg=4: self.moveLeg(value, point, leg))

        self.horizontalSlider_9.valueChanged.connect(self.translateXAxis)
        self.horizontalSlider_7.valueChanged.connect(self.translateYAxis)
        self.horizontalSlider_8.valueChanged.connect(self.translateZAxis)

        self.horizontalSlider_12.valueChanged.connect(self.rotationX)
        self.horizontalSlider_10.valueChanged.connect(self.rotationY)
        self.horizontalSlider_11.valueChanged.connect(self.rotationZ)

        self.horizontalSlider_25.valueChanged.connect(self.handleBodyRadius)
        self.pushButton.clicked.connect(self.resetValues)
        self.pushButton_2.clicked.connect(self.animateLegRaise)

        self.radioButton.toggled.connect(self.handleRadioButtonChange)
        # self.radioButton_2.toggled.connect(self.handleToggleTrajectory)

        self.horizontalSlider_24.valueChanged.connect(
            lambda value, leg="coxa": self.handleBodyLegLengthChange(value, leg))
        self.horizontalSlider_22.valueChanged.connect(
            lambda value, leg="tibia": self.handleBodyLegLengthChange(value, leg))
        self.horizontalSlider_23.valueChanged.connect(
            lambda value, leg="femur": self.handleBodyLegLengthChange(value, leg))

        self.pushButton_3.clicked.connect(self.clearGraph)
        self.pushButton_10.clicked.connect(self.animateLegCurve)
        self.pushButton_11.clicked.connect(self.simulationSolutionSpace)

    def clearGraph(self):
        self.ax.cla()
        plt.draw()

    def setXPoint(self, value, leg):
        if leg == 1:
            self.label_4.setText(str(value))
            self.xPoint[0] = value
            print(value, leg)
        elif leg == 2:
            self.label_34.setText(str(value))
            self.xPoint[1] = value
            print(value, leg)
        elif leg == 3:
            self.label_28.setText(str(value))
            self.xPoint[2] = value
            print(value, leg)
        else:
            self.label_40.setText(str(value))
            self.xPoint[3] = value
            print(value, leg)

    def setYPoint(self, value, leg):
        if leg == 1:
            self.label_5.setText(str(value))
            self.yPoint[0] = value
        elif leg == 2:
            self.label_38.setText(str(value))
            self.yPoint[1] = value
        elif leg == 3:
            self.label_32.setText(str(value))
            self.yPoint[2] = value
        else:
            self.label_44.setText(str(value))
            self.yPoint[3] = value

    def setZPoint(self, value, leg):
        if leg == 1:
            self.label_6.setText(str(value))
            self.zPoint[0] = value
        elif leg == 2:
            self.label_36.setText(str(value))
            self.zPoint[1] = value
        elif leg == 3:
            self.label_30.setText(str(value))
            self.zPoint[2] = value
        else:
            self.label_42.setText(str(value))
            self.zPoint[3] = value

    def moveLeg(self, value, point, leg):

        if point == "x":
            self.setXPoint(value, leg)
            self.renderGraph()
        elif point == "y":
            self.setYPoint(value, leg)
            self.renderGraph()
        elif point == "z":
            self.setZPoint(value, leg)
            self.renderGraph()

    def handleBodyLegLengthChange(self, e, value):
        if value == "coxa":
            self.label_46.setText(str(e))
            self.coxaLength = e
            self.renderGraph()
        elif value == "tibia":
            self.label_50.setText(str(e))
            self.tibiaLength = e
            self.renderGraph()
        else:
            self.label_48.setText(str(e))
            self.femurLength = e
            self.renderGraph()

    def handleBodyRadius(self, value):
        self.radius = value
        self.label_53.setText(str(self.radius))
        self.renderGraph()

    def handleToggleTrajectory(self):
        self.trajectory = self.radioButton_2.isChecked()
        self.renderGraph()

    def handleIncrement(self, value):
        if value == "x":
            x = self.pointX + 5
            self.setXPos(x)
            # self.serialObj.write(ord('+'))
        if value == "y":
            y = self.pointY + 5
            self.setYPos(y)
            #self.serialObj.write(bytearray(['+', '+']))
        if value == "z":
            z = self.pointZ + 5
            self.setZPos(z)
            # self.serialObj.write(ord('+++'))

    def handleDecrement(self, value):
        if value == "x":
            x = self.pointX - 5
            self.setXPos(x)
            # self.serialObj.write(ord('-'))
        if value == "y":
            y = self.pointY - 5
            self.setYPos(y)
            # self.serialObj.write(ord('--'))
        if value == "z":
            z = self.pointZ - 5
            self.setZPos(z)
            # self.serialObj.write(ord('---'))

    def handleRadioButtonChange(self):
        self.trace = self.radioButton.isChecked()

    def moveLegOne(self, x, y, z):
        self.setXPoint(x, 1)
        self.setYPoint(y, 1)
        self.setZPoint(z, 1)
        self.renderGraph()

    def moveLegTwo(self, x, y, z):
        self.setXPoint(x, 2)
        self.setYPoint(y, 2)
        self.setZPoint(z, 2)
        self.renderGraph()

    def moveLegThree(self, x, y, z):
        self.setXPoint(x, 3)
        self.setYPoint(y, 3)
        self.setZPoint(z, 3)
        self.renderGraph()

    def moveLegFour(self, x, y, z):
        self.setXPoint(x, 4)
        self.setYPoint(y, 4)
        self.setZPoint(z, 4)
        self.renderGraph()

    def setXTranslate(self, pos):
        self.translateX = pos
        self.horizontalSlider_9.setValue(self.translateX)
        self.label_13.setText(str(pos))

    def setYTranslate(self, pos):
        self.translateY = pos
        self.horizontalSlider_7.setValue(self.translateY)
        self.label_17.setText(str(pos))

    def setZTranslate(self, pos):
        self.translateZ = pos
        self.horizontalSlider_8.setValue(self.translateZ)
        self.label_15.setText(str(pos))

    def setXRotate(self, pos):
        self.rotX = pos
        self.horizontalSlider_12.setValue(self.rotX)
        self.label_19.setText(str(pos))

    def setYRotate(self, pos):
        self.rotY = pos
        self.horizontalSlider_10.setValue(self.rotY)
        self.label_23.setText(str(pos))

    def setZRotate(self, pos):
        self.rotZ = pos
        self.horizontalSlider_11.setValue(self.rotZ)
        self.label_21.setText(str(pos))

    def getEquidistantPoints(self, p1, p2, parts):
        return zip(np.linspace(p1[0], p2[0], parts+1),
                   np.linspace(p1[1], p2[1], parts+1))

    def simulationSolutionSpace(self):
        data_points = 20
        pass
        # plt.pause(0.0001)

    def animateLegCurve(self):
        x = 100
        buffer = []
        data_points = 3
        for x in range(0, 5):
            for q in range(1, data_points):
                data = list(self.getEquidistantPoints(
                    (80, 50), (80, 25), data_points))
                data2 = list(self.getEquidistantPoints(
                    (80, 50), (80, 25), data_points))

                self.moveLegOne(80, data[q][0], data[q][1])
                self.moveLegTwo(80, data2[q][0], data2[q][1])

                data3 = list(self.getEquidistantPoints(
                    (80, 50), (80, 80), data_points))
                data4 = list(self.getEquidistantPoints(
                    (80, 50), (80, 80), data_points))

                self.moveLegThree(80, data3[q][0], data3[q][1])
                self.moveLegFour(80, data4[q][0], data4[q][1])

                plt.pause(0.00001)

            for q in range(1, data_points):
                data = list(self.getEquidistantPoints(
                    (80, 50), (40, 50), data_points))
                data2 = list(self.getEquidistantPoints(
                    (80, 50), (120, 50), data_points))
                self.moveLegOne(80, data[q][0], data[q][1])
                self.moveLegTwo(80, data2[q][0], data2[q][1])

                data3 = list(self.getEquidistantPoints(
                    (80, 80), (40, 80), data_points))
                data4 = list(self.getEquidistantPoints(
                    (80, 80), (120, 80), data_points))

                self.moveLegThree(80, data3[q][0], data3[q][1])
                self.moveLegFour(80, data4[q][0], data4[q][1])

                plt.pause(0.00001)

            for q in range(1, data_points):
                data = list(self.getEquidistantPoints(
                    (40, 50), (40, 50), data_points))
                data2 = list(self.getEquidistantPoints(
                    (120, 50), (120, 50), data_points))
                self.moveLegOne(80, data[q][0], data[q][1])
                self.moveLegTwo(80, data2[q][0], data2[q][1])

                data3 = list(self.getEquidistantPoints(
                    (40, 80),  (40, 50),  data_points))
                data4 = list(self.getEquidistantPoints(
                    (120, 80), (120, 50), data_points))
                self.moveLegThree(80, data3[q][0], data3[q][1])
                self.moveLegFour(80,  data4[q][0], data4[q][1])
                plt.pause(0.00001)

            for q in range(1, data_points):
                data = list(self.getEquidistantPoints(
                    (40, 50), (80, 50), data_points))
                data2 = list(self.getEquidistantPoints(
                    (120, 50), (80, 50), data_points))
                self.moveLegOne(80, data[q][0], data[q][1])
                self.moveLegTwo(80, data2[q][0], data2[q][1])

                data3 = list(self.getEquidistantPoints(
                    (40, 50), (80, 50), data_points))
                data4 = list(self.getEquidistantPoints(
                    (120, 50), (80, 50), data_points))
                self.moveLegThree(80, data3[q][0], data3[q][1])
                self.moveLegFour(80, data4[q][0], data4[q][1])

                plt.pause(0.00001)

    def animateLegRaise(self):
        speed = 2
        total_points = 100

        """
        pos-1 = 70, 70, 50
        pos-2 = 70, 50, 50
        pos-3 = 70, 50, 70
        pos-4 = 70, 70, 70
        pos-5 = 45, 100, -10
      """
        stride_length_start = 60
        stride_length_end = 120

        stride_height_start = 30
        stride_height_end = 50
        stride_length = [stride_length_start+self.translateY,
                         stride_length_end+self.translateY]
        stride_height = [stride_height_start+self.translateZ,
                         stride_height_end+self.translateZ]

        self.moveLegOne(70, stride_length[0], stride_height[0])
        for x in range(0, 60):
            self.moveLegOne(70, stride_length[1]-x, stride_height[0])
            plt.pause(0.0001)

        for x in range(0, 20):
            self.moveLegOne(70, stride_length[0], stride_height[0]+x)
            plt.pause(0.00001)

        for x in range(0, 60):
            self.moveLegOne(70, stride_length[0]+x, stride_height[1])
            plt.pause(0.00001)

        for x in range(0, 20):
            self.moveLegOne(70, stride_length[1], stride_height[1]-x)
            plt.pause(0.0001)

        # for x in range(45, 85):
        #   self.moveLegOne(80, 80, x)
        #   self.moveLegTwo(80, 80, x)
        #   self.moveLegFour(80, 80, 85-x)
        #   self.moveLegThree(80,80, 85-x)
        #   plt.pause(0.0001)

        # for x in range(45, 85):
        #   self.moveLegOne(80, 80, 85-x)
        #   self.moveLegThree(80,80, x)
        #   self.moveLegTwo(80, 80, x)
        #   self.moveLegFour(80, 80, 85-x)
        #   plt.pause(0.0001)

    def renderGraph(self):
        rotatedPoints_1 = handleRotate(
            theta_1=-self.rotX,
            theta_2=-self.rotY,
            theta_3=self.rotZ,
            x=self.xPoint[0],
            y=self.yPoint[0],
            z=self.zPoint[0]
        )
        rotatedPoints_2 = handleRotate(
            theta_1=self.rotX,
            theta_2=self.rotY,
            theta_3=self.rotZ,
            x=self.xPoint[1],
            y=self.yPoint[1],
            z=self.zPoint[1]
        )
        rotatedPoints_3 = handleRotate(
            theta_1=-self.rotX,
            theta_2=self.rotY,
            theta_3=self.rotZ,
            x=self.xPoint[2],
            y=self.yPoint[2],
            z=self.zPoint[2]
        )
        rotatedPoints_4 = handleRotate(
            theta_1=self.rotX,
            theta_2=-self.rotY,
            theta_3=self.rotZ,
            x=self.xPoint[3],
            y=self.yPoint[3],
            z=self.zPoint[3]
        )

        points_1 = (
            getIKPoint(
                rotatedPoints_1[0] - self.translateX,
                rotatedPoints_1[1] - self.translateY,
                rotatedPoints_1[2] + self.translateZ
            ))
        print(points_1)

        points_2 = (
            getIKPoint(
                rotatedPoints_2[0] + self.translateX,
                rotatedPoints_2[1] + self.translateY,
                rotatedPoints_2[2] + self.translateZ
            ))

        points_3 = (
            getIKPoint(
                rotatedPoints_3[0] - self.translateX,
                rotatedPoints_3[1] + self.translateY,
                rotatedPoints_3[2] + self.translateZ
            ))

        points_4 = (
            getIKPoint(
                rotatedPoints_4[0] + self.translateX,
                rotatedPoints_4[1] - self.translateY,
                rotatedPoints_4[2] + self.translateZ
            ))

        self.dial.setValue(points_1[0])
        self.dial_2.setValue(points_1[1])
        self.dial_3.setValue(points_1[2])
        self.label_7.setText(str(points_1[0]))
        self.label_8.setText(str(points_1[1]))
        self.label_9.setText(str(points_1[2]))

        plotFrame(
            [points_1[0], points_2[0], points_3[0], points_4[0]],
            [points_1[1], points_2[1], points_3[1], points_4[1]],
            [points_1[2], points_2[2], points_3[2], points_4[2]],
            self.ax, self.trace, self.radius,
            self.coxaLength, self.tibiaLength, self.femurLength
        )

        plt.draw()

    def resetValues(self):
        print("Reseting to Home position")

        self.setXTranslate(0)
        self.setYTranslate(0)
        self.setZTranslate(0)

        self.setXRotate(0)
        self.setYRotate(0)
        self.setZRotate(0)

        self.moveLegOne(80, 80, 80)
        self.moveLegTwo(80, 80, 80)
        self.moveLegThree(80, 80, 80)
        self.moveLegFour(80, 80, 80)
        self.renderGraph()

    def rotationX(self, value):
        self.setXRotate(value)
        self.renderGraph()

    def rotationY(self, value):
        self.setYRotate(value)
        self.renderGraph()

    def rotationZ(self, value):
        self.setZRotate(value)
        self.renderGraph()

    def translateXAxis(self, value):
        self.setXTranslate(value)
        self.renderGraph()

    def translateYAxis(self, value):
        self.setYTranslate(value)
        self.renderGraph()

    def translateZAxis(self, value):
        self.setZTranslate(value)
        self.renderGraph()

    def movePointX(self, value):
        self.setXPos(value)
        self.renderGraph()

    def movePointY(self, value):
        self.setYPos(value)
        self.renderGraph()

    def movePointZ(self, value):
        self.setZPos(value)
        self.renderGraph()

    def run(self):
        self.body = plt.figure("Full Body IK")
        self.ax = plt.axes([0.05, 0.2, 0.90, 0.75], projection="3d")
        # self.canvas = FigureCanvas(self.body)
        # self.gridLayout.addWidget(self.canvas)

        # self.topXY = plt.figure("TOP View")
        # self.ax2 = self.topXY.add_subplot(111)
        # self.canvas2 = FigureCanvas(self.topXY)
        # self.gridLayout_2.addWidget(self.canvas2)

        # self.sideXZ = plt.figure("Side XZ")
        # self.ax3 = self.sideXZ.add_subplot(111)
        # self.canvas3 = FigureCanvas(self.sideXZ)
        # self.gridLayout_3.addWidget(self.canvas3)

        # self.canvas.draw()
        # self.canvas2.draw()
        # self.canvas3.draw()
        plt.show()
        self.renderGraph()


def main():
    app = QApplication(sys.argv)
    widget = App()
    widget.show()
    widget.run()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
