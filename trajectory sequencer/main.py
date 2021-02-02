import copy
import time
import sys
import json
import glob
import time
import random
import numpy as np

from robot_model import *

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


class App(QDialog):
    def __init__(self):
        super(App, self).__init__()
        try:
            loadUi('main.ui', self)
        except Exception as e:
            print(e)
            print("main.ui could not be found!")

        self.sliders = [
          self.x_slider_1, 
          self.x_slider_3,
          self.x_slider_4,
          self.x_slider_5,
          self.y_slider_1,
          self.y_slider_3,
          self.y_slider_4,
          self.y_slider_5,
          self.z_slider_1,
          self.z_slider_3,
          self.z_slider_4,
          self.z_slider_5
        ] 


        self.buttons = [
          [self.x_decrement_1, self.x_increment_1],
          [self.x_decrement_3, self.x_increment_3],
          [self.x_decrement_4, self.x_increment_4],
          [self.x_decrement_5, self.x_increment_5],

          [self.y_decrement_1, self.y_increment_1],
          [self.y_decrement_3, self.y_increment_3],
          [self.y_decrement_4, self.y_increment_4],
          [self.y_decrement_5, self.y_increment_5],

          [self.z_decrement_1, self.z_increment_1],
          [self.z_decrement_3, self.z_increment_3],
          [self.z_decrement_4, self.z_increment_4],
          [self.z_decrement_5, self.z_increment_5]
        ]


        self.host: str = ""
        self.port: int = 0 
        self.activationStatus: bool = True
        self.robotMode:int = 1

        self.robotModel: RobotModel = RobotModel(
                           host=self.host, 
                           port=self.port, 
                           activate=self.activationStatus, 
                           mode=self.robotMode, 
                           robotName="Macha")
        
        
        print(self.robotModel.printRobotCredentials())
        # #Setting the sliders to the lambda functions
        # counter:int  = 0
        # for x in range(len(self.buttons)):
        #   for y in range(len(x)):
        #     self.buttons[x][y].clicked.connect(lambda x=x, y=y: self.handleButtonClick(x, y))



        #Setting button
        button_counter = 0
        for x in range(len(self.buttons)):
          for y in range(len(self.buttons[x])):
            self.buttons[x][y].clicked.connect(lambda value="1", 
            decrement=x, 
            increment=y, 
            level_counter=button_counter: self.handleButtonClick(
              decrement, increment, button_counter))
          button_counter += 1


    def handleButtonClick(self, x, y, button_counter):
      
      if x == 0 or x == 1 or x == 2 or x == 3:
        if y:
          if x == 0:
            self.robotModel.leg_1.x += 1
          elif x == 1:
            self.robotModel.leg_2.x += 1
          elif x == 2:
            self.robotModel.leg_3.x += 1
          else:
            self.robotModel.leg_4.x += 1
        else:
          if x == 0:
            self.robotModel.leg_1.x -= 1
          elif x == 1:
            self.robotModel.leg_2.x -= 1
          elif x == 2:
            self.robotModel.leg_3.x -= 1
          else:
            self.robotModel.leg_4.x -= 1
      
      elif x == 4 or x == 5 or x == 6 or x == 7:
        if y:
          if x == 4:
            self.robotModel.leg_1.y += 1
          elif x == 5:
            self.robotModel.leg_2.y += 1
          elif x == 6:
            self.robotModel.leg_3.y += 1
          else:
            self.robotModel.leg_4.y += 1
        else:
          if x == 4:
            self.robotModel.leg_1.y -= 1
          elif x == 5:
            self.robotModel.leg_2.y -= 1
          elif x == 6:
            self.robotModel.leg_3.y -= 1
          else:
            self.robotModel.leg_4.y -= 1

      elif x == 8 or x == 9 or x == 10 or x == 11:
        if y:
          if x == 8:
            self.robotModel.leg_1.z += 1
          elif x == 9:
            self.robotModel.leg_2.z += 1
          elif x == 10:
            self.robotModel.leg_3.z += 1
          else:
            self.robotModel.leg_4.z += 1
        else:
          if x == 8:
            self.robotModel.leg_1.z -= 1
          elif x == 9:
            self.robotModel.leg_2.z -= 1
          elif x == 10:
            self.robotModel.leg_3.z -= 1
          else:
            self.robotModel.leg_4.z -= 1
        
      print(self.robotModel.leg_1.show())
      print(self.robotModel.leg_2.show())
      print(self.robotModel.leg_3.show())
      print(self.robotModel.leg_4.show())

    def handleSlider(self, value, counter):
      print(value, counter)

    def run(self):
        pass


def main():
    app = QApplication(sys.argv)
    widget = App()
    widget.show()
    widget.run()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
