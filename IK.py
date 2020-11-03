from   matplotlib.widgets   import Slider, RadioButtons
from   mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from   itertools import product
import numpy as np
import math
import time

x_val = 90
y_val = 90
z_val = 90

rotationX = 0

LINK_1 = 60
LINK_2 = 120
LINK_3 = 60

fig = plt.figure("IK")


ax = plt.axes([0.05, 0.2, 0.90, 0.75], projection="3d")

axxval = plt.axes([0.35, 0.1, 0.45, 0.03])
a0_val = Slider(axxval, "X", -300, 300, valinit=x_val)

axyval = plt.axes([0.35, 0.0575, 0.45, 0.03])
a1_val = Slider(axyval, "Y", -300, 300, valinit=y_val)

axzval = plt.axes([0.35, 0.015, 0.45, 0.03])
a2_val = Slider(axzval, "Z", -300, 300, valinit=z_val)

rotX = plt.axes([0.40, 0.010, 0.45, 0.03])
rotX_val = Slider(rotX, "RotX", -180, 180, valinit=rotationX)


def getIKPoint(x, y, z):
  try: 
    theta_1 = math.atan2(y, x)
    A = z 
    B = math.cos(theta_1) * x + y + math.sin(theta_1) - LINK_1 
    C = (
          math.pow(A, 2) + 
          math.pow(B, 2) - 
          math.pow(LINK_3, 2) - 
          math.pow(LINK_2, 2)
          ) / (2 * LINK_3 * LINK_2)  
    theta_3 = math.atan2(math.sqrt(1 - math.pow(C, 2)), C)
    D = math.cos(theta_3) * LINK_3 + LINK_2 
    E = math.sin(theta_3) * LINK_3 

    numerator = (A * D - B * E) / (math.pow(E, 2) + math.pow(D, 2))
    denominator = 1 - math.pow(numerator, 2)
    theta_2 = math.atan2(numerator, math.sqrt(denominator))

    theta_1 = np.degrees(theta_1)
    theta_2 = np.degrees(theta_2) 
    theta_3 = np.degrees(theta_3)

  except ValueError as exc:
    print(exc)
    return [0, 0, 0]
  return [theta_1, theta_2, theta_3] 


def points_in_circle(radius):
    for x, y in product(range(int(radius) + 1), repeat=2):
        if x**2 + y**2 <= radius**2:
            yield from set(((x, y), (x, -y), (-x, y), (-x, -y),))



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
  

def handleRotate(
  theta_1:int, theta_2:int, 
  theta_3:int, x:int, 
  y:int, z:int ):

  theta_1 = math.radians(theta_1)
  theta_2 = math.radians(theta_2)
  theta_3 = math.radians(theta_3)

  rotationMatrix = np.array([
      y *
        (
          math.cos(theta_1) * math.sin(theta_3) +
          math.cos(theta_3) * math.sin(theta_1) * 
          math.sin(theta_2)
        ) +
        z *
          (
            math.sin(theta_1) * math.sin(theta_3) -
            math.cos(theta_1) * math.cos(theta_3) * 
            math.sin(theta_2)
            ) +
        x * 
        math.cos(theta_2) * 
        math.cos(theta_3), 
        # First set of equations. 
      y *
        (
          math.cos(theta_1) *
          math.cos(theta_3) -
          math.sin(theta_1) * 
          math.sin(theta_2) * 
          math.sin(theta_3)
        ) +
        z *
          (
            math.cos(theta_3) * 
            math.sin(theta_1) +
            math.cos(theta_1) * 
            math.sin(theta_2) * 
            math.sin(theta_3)
          ) -
        x * 
        math.cos(theta_2) * 
        math.sin(theta_3),
        # Second set of equations.
      x * 
        math.sin(theta_2) +
        z * math.cos(theta_1) * math.cos(theta_2) -
        y * math.cos(theta_2) * math.sin(theta_1),
    ])
  return rotationMatrix


def plotFrame( theta_1, theta_2, theta_3, pltObj ):  
  frame = ( getFKFrame(
              np.radians(theta_1), 
              np.radians(theta_2), 
              np.radians(theta_3)) )
    
  pltObj.cla() 
  pltObj.plot( 
        [0, frame[0][0][3], frame[1][0][3], frame[2][0][3]], 
        [0, frame[0][1][3], frame[1][1][3], frame[2][1][3]], 
        [0, frame[0][2][3], frame[1][2][3], frame[2][2][3]], 
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
    points = (getIKPoint(x_val, y_val, z_val))
    print(points)
    plotFrame(points[0], points[1], points[2], ax)
    
    

def update_a1_val(val):
    global x_val, y_val, z_val
    y_val = val
    points = (getIKPoint(x_val, y_val, z_val))
    print(points)
    plotFrame(points[0], points[1], points[2], ax)
    

def update_a2_val(val):
    global x_val, y_val, z_val
    z_val = val
    points = (getIKPoint(x_val, y_val, z_val))
    print(points)
    plotFrame(points[0], points[1], points[2], ax)


a0_val.on_changed( update_a0_val )
a1_val.on_changed( update_a1_val )
a2_val.on_changed( update_a2_val )

for x in range(0, 100):
  print( handleRotate( 0, 0, 0, 100, 120, 150 ) )
  servo_angles = getIKPoint(x_val, y_val, x)
  plotFrame(servo_angles[0], servo_angles[1], servo_angles[2], ax)
  plt.pause(0.1)

plt.show()




