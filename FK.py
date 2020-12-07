from matplotlib.widgets import Slider, RadioButtons
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import math


x_val = 90
y_val = 90
z_val = 90

LINK_1 = 60
LINK_2 = 120
LINK_3 = 110


fig = plt.figure("FK")
ax = plt.axes([0.05, 0.2, 0.90, 0.75], projection="3d")
axe = plt.axes([0.25, 0.85, 0.001, 0.001])

axxval = plt.axes([0.35, 0.1, 0.45, 0.03])
a0_val = Slider(axxval, "Theta 1", 0, 180, valinit=x_val)

axyval = plt.axes([0.35, 0.0575, 0.45, 0.03])
a1_val = Slider(axyval, "Theta 2", 0, 180, valinit=y_val)

axzval = plt.axes([0.35, 0.015, 0.45, 0.03])
a2_val = Slider(axzval, "Theta 3", 0, 180, valinit=z_val)



def getFKFrame(theta_1, theta_2, theta_3):
  T01 = np.array(
                [
                  [math.cos(theta_1), -math.sin(theta_1), 0, 0], 
                  [ math.sin(theta_1), math.cos(theta_1), 0, 0 ], 
                  [ 0, 0, 1, 0], 
                  [ 0, 0, 0, 1]
                 ] 
                 )

  T02 = np.array(
                 [
                  [math.cos(theta_2), -math.sin(theta_2), 0, LINK_1],
                  [0, 0, -1, 0],
                  [math.sin(theta_2), math.cos(theta_2), 0, 0],
                  [0, 0, 0, 1]
                 ]
                )

  T03 = np.array(
                 [
                  [math.cos(theta_3), -math.sin(theta_3), 0, LINK_2],
                  [math.sin(theta_3), math.cos(theta_3), 0, 0],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1]
                 ]
                )

  T04 = np.array(
                 [
                   [1, 0, 0, LINK_3],
                   [0, 1, 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]
                  ]
                )

  T10 = np.dot(T01, T02)
  T20 = np.dot(T10, T03)
  T30 = np.dot(T20, T04)

  return [T10, T20, T30]
  

def plotFrame( theta_1, theta_2, theta_3, pltObj ):
  frame = ( getFKFrame(
              np.radians(theta_1), 
              np.radians(-theta_2 ), 
              np.radians(-theta_3 )) )
  print(frame[2][0][3], frame[2][1][3], frame[2][2][3])
  pltObj.cla() 
  pltObj.plot( 
        [0, frame[0][0][3], frame[1][0][3],frame[2][0][3]], 
        [0, frame[0][1][3], frame[1][1][3],frame[2][1][3]], 
        [0, frame[0][2][3], frame[1][2][3],frame[2][2][3]], 
        "o-", 
        markerSize=5, 
        markerFacecolor="orange", 
        linewidth=5, 
        color="blue" 
    )
    
  pltObj.set_xlim3d(-200, 200)
  pltObj.set_ylim3d(-200, 200)
  pltObj.set_zlim3d(-100, 200)
  pltObj.set_xlabel("X-axis")
  pltObj.set_ylabel("Y-axis")
  pltObj.set_zlabel("Z-axis")
  pltObj.set_axisbelow(True)

def update_a0_val(val):
    global x_val , y_val, z_val
    x_val = val
    plotFrame(x_val, y_val, z_val, ax)

def update_a1_val(val):
    global x_val, y_val, z_val
    y_val = val
    plotFrame(x_val, y_val, z_val, ax)

def update_a2_val(val):
    global x_val, y_val, z_val
    z_val = val
    plotFrame(x_val, y_val, z_val, ax)


a0_val.on_changed( update_a0_val )
a1_val.on_changed( update_a1_val )
a2_val.on_changed( update_a2_val )


plotFrame(x_val, y_val, z_val, ax)
plt.show()




