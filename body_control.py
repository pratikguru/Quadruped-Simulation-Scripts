from matplotlib.widgets import Slider, RadioButtons
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from itertools import product
import serial
import numpy as np
import math
import time


x_val = 90
y_val = 90
z_val = 90

LINK_1 = 60
LINK_2 = 120
LINK_3 = 60

fig = plt.figure("IK")
ax = plt.axes([0.05, 0.2, 0.90, 0.75], projection="3d")


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


def getFKFrame(theta_1, theta_2, theta_3):

    T01 = np.array(
        [
            [math.cos(theta_1), -math.sin(theta_1), 0, 0],
            [math.sin(theta_1), math.cos(theta_1), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
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
        theta_1: int, theta_2: int,
        theta_3: int, x: int,
        y: int, z: int):

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


def plotFrame(theta_1, theta_2, theta_3, pltObj, linecolor):
    #theta_1 = (np.interp(theta_1, [-180, 180], [0, 180]))
    #theta_2 = (np.interp(-theta_2, [-180, 180], [0, 180]))
    #theta_3 = (np.interp(-theta_3, [-180, 180], [0, 180]))
    frame = (getFKFrame(
        np.radians(theta_1),
        np.radians((-theta_2)),
        np.radians((-theta_3))))

    pltObj.plot(
        [0, frame[0][0][3], frame[1][0][3], frame[2][0][3]],
        [0, frame[0][1][3], frame[1][1][3], frame[2][1][3]],
        [0, frame[0][2][3], frame[1][2][3], frame[2][2][3]],
        "o-",
        markerSize=2,
        markerFacecolor="orange",
        linewidth=3,
        color=linecolor
    )

    pltObj.set_xlim3d(-200, 200)
    pltObj.set_ylim3d(-200, 200)
    pltObj.set_zlim3d(-100, 200)
    pltObj.set_xlabel("X-axis")
    pltObj.set_ylabel("Y-axis")
    pltObj.set_zlabel("Z-axis")
    pltObj.set_axisbelow(True)


if __name__ == "__main__":
    print("Script Starting.")

    rPoints = handleRotate(0, 0, 90, -100, -100, 0)
    rPoints2 = handleRotate(0, 0, 180, -100, -100, 0)
    rPoints3 = handleRotate(0, 0, 270, -100, 100, 0)
    rPoints4 = handleRotate(0, 0, 300, -100, 100, 0)

    points = getIKPoint(rPoints[0], rPoints[1], rPoints[2])
    points2 = getIKPoint(rPoints2[0], rPoints2[1], rPoints2[2])
    points3 = getIKPoint(rPoints3[0], rPoints3[1], rPoints3[2])
    points4 = getIKPoint(rPoints4[0], rPoints4[1], rPoints4[2])

    plotFrame(points[0],  points[1],  points[2],  ax, "red")
    plotFrame(points2[0], points2[1], points2[2], ax, "blue")
    plotFrame(points3[0], points3[1], points3[2], ax, "green")
    plotFrame(points4[0], points4[1], points4[2], ax, "orange")

    plt.pause(0.001)
    plt.show()
