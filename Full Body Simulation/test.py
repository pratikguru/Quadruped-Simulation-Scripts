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
    from   PyQt5           import QtCore
    from   PyQt5.QtCore    import pyqtSlot
    from   PyQt5           import QtWidgets, QtGui
    from   PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox
    from   PyQt5.QtWidgets import *
    from   PyQt5.uic       import loadUi
    from   matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from   matplotlib.figure import Figure
except Exception as e:
    print ("Requirement Error! The PyQt Libs are not installed.")
    import os
import math
import matplotlib.pyplot as plt



class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        try:
            loadUi('test.ui', self)
        except Exception as e:
            print (e)
            print ("main.ui could not be found!")
        
        self.pointX = -130
        self.pointY = -120
        self.pointZ = 0

        self.translateX = 0
        self.translateY = 0
        self.translateZ = 0

        self.rotX = 0
        self.rotY = 0
        self.rotZ = 0 

        self.setXPos(self.pointX)
        self.setYPos(self.pointY)
        self.setZPos(self.pointZ)

        self.setXTranslate(self.translateX)
        self.setYTranslate(self.translateY)
        self.setZTranslate(self.translateZ) 


        self.setXRotate(self.rotX)
        self.setYRotate(self.rotY)
        self.setZRotate(self.rotZ)
 

        self.horizontalSlider.valueChanged.connect(self.movePointX)
        self.horizontalSlider_2.valueChanged.connect(self.movePointY)
        self.horizontalSlider_3.valueChanged.connect(self.movePointZ) 


        self.horizontalSlider_9.valueChanged.connect(self.translateXAxis)
        self.horizontalSlider_7.valueChanged.connect(self.translateYAxis)
        self.horizontalSlider_8.valueChanged.connect(self.translateZAxis)

        self.horizontalSlider_12.valueChanged.connect(self.rotationX)
        self.horizontalSlider_10.valueChanged.connect(self.rotationY)
        self.horizontalSlider_11.valueChanged.connect(self.rotationZ)


        self.pushButton.clicked.connect(self.resetValues)
        self.pushButton_2.clicked.connect(self.animateLegRaise)
        

    def setXPos(self, pos):
      self.pointX = pos
      self.horizontalSlider.setValue(self.pointX)
      self.label_4.setText(str(pos))

    def setYPos(self, pos):
      self.pointY = pos 
      self.horizontalSlider_2.setValue(self.pointY)
      self.label_5.setText(str(pos))

    def setZPos(self, pos):
      self.pointZ = pos 
      self.horizontalSlider_3.setValue(self.pointZ)
      self.label_6.setText(str(pos))

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

    def animateLegRaise(self):
      self.setXPos(85)
      self.setYPos(85)
      self.setZPos(120)
      self.renderGraph()
        
            

    def renderGraph(self):
      rotatedPoints = handleRotate(
            theta_1 = self.rotX,
            theta_2 = self.rotY,
            theta_3 = self.rotZ,
            x = self.pointX , 
            y = self.pointY, 
            z = self.pointZ
        )

      points = (
        getIKPoint( 
          rotatedPoints[0] - self.translateX,
          rotatedPoints[1] - self.translateY,
          rotatedPoints[2] - self.translateZ
      ))

      plotFrame( points[0], points[1], points[2], self.ax)
      plotFrame2DXY(points[0], points[1], points[2], self.ax2)
      plotFrame2DXZ(points[0], points[1], points[2], self.ax3)
      self.canvas.draw()
      self.canvas2.draw()
      self.canvas3.draw()
      



    def resetValues(self):
      print ("Reseting to Home position")
      self.setXPos(0)
      self.setYPos(0)
      self.setZPos(0)

      self.setXTranslate(0)
      self.setYTranslate(0)
      self.setZTranslate(0) 


      self.setXRotate(0)
      self.setYRotate(0)
      self.setZRotate(0)
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
      self.canvas = FigureCanvas(self.body)
      self.gridLayout.addWidget(self.canvas)


      self.topXY = plt.figure("TOP View")
      self.ax2 = self.topXY.add_subplot(111)
      self.canvas2 = FigureCanvas(self.topXY)
      self.gridLayout_2.addWidget(self.canvas2)

      self.sideXZ = plt.figure("Side XZ")
      self.ax3 = self.sideXZ.add_subplot(111)
      self.canvas3 = FigureCanvas(self.sideXZ)
      self.gridLayout_3.addWidget(self.canvas3)

      
      self.canvas.draw()
      self.canvas2.draw()
      self.canvas3.draw()

      self.renderGraph()
      



       


def main():
    app = QApplication(sys.argv)
    widget = App()
    widget.show()
    widget.run()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()