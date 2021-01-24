import socket
import os
import pprint
import pygame
import numpy as np
import copy
import glob
import time
import numpy as np
import math
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

"""
Solution space.

[0, 0, 0, 0, 40, 0, -40, 0,  40, 0, -40, 0],
[60, 0, 60, 0, 20, 0,  20, 0,  20, 0, 20, 0],
[40, 0, 75, 0, 40, 0,  40, 0,  75, 0, 75, 0],


"""


class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""
    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    def init(self):
        """Initialize the joystick components"""

        pygame.init()
        pygame.joystick.init()
        self.axisMode = False
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
        self.window_size: int = 100
        self.button_states = {
            0: "s",
            1: "x",
            2: "o",
            3: "t",
            4: "l1",
            5: "r1",
            6: "l2",
            7: "r2",
            8: "share",
            9: "option",
            10: "l3",
            11: "r3",
            12: "home",
            13: "pad",
        }

    def _smooth(self, value: float, smooth: int) -> int:
        sum = 0
        for x in range(0, smooth):
            sum += value

        return int(sum/smooth)

    def smoother(self, y, box_pts):
        box = np.ones(box_pts)/box_pts
        y_smooth = np.convolve(y, box, mode='same')
        return y_smooth

    def listen(self):
        """Listen for events to happen"""

        if not self.axis_data:
            self.axis_data = {}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                self.axis_data[event.axis] = round(event.value, 2)
            elif event.type == pygame.JOYBUTTONDOWN:
                self.button_data[event.button] = True
            elif event.type == pygame.JOYBUTTONUP:
                self.button_data[event.button] = False
            elif event.type == pygame.JOYHATMOTION:
                self.hat_data[event.hat] = event.value

        new_dict = {}
        for key, value in self.button_states.items():
            try:
                new_dict[value] = self.button_data[key]
            except KeyError as e:
                new_dict[value] = 1
        try:
            new_dict["up"] = self.hat_data[0][1]
            new_dict["down"] = self.hat_data[0][1]

            new_dict["right"] = self.hat_data[0][0]
            new_dict["left"] = self.hat_data[0][0]

            new_dict["left_x"] = self.axis_data[0]
            new_dict["left_y"] = self.axis_data[1]

            new_dict["right_x"] = self.axis_data[2]
            new_dict["right_y"] = self.axis_data[5]

            new_dict["l2_a"] = self.axis_data[3]
            new_dict["r2_a"] = self.axis_data[4]
        except KeyError as e:
            print("Roll Sticks to continue!")
        return (new_dict)


def _map(x, in_min, in_max, out_min, out_max) -> int:
    return int((x-in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def _smooth(value: float, smooth: int) -> int:
    sum = 0
    for x in range(0, smooth):
        sum += _map(value, -1, 1, 0, 500)
    return int(sum/smooth)


def smoother(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth


if __name__ == "__main__":
    ps4 = PS4Controller()
    ps4.init()

    fig = plt.figure("IK")
    ax = plt.axes([0.05, 0.2, 0.90, 0.75], projection="3d")

    while True:
        os.system("clear")
        # pprint.pprint(ps4.listen())

        inputs = ps4.listen()
        data: int = 0

        try:
            ax.set_xlim3d(-50, 50)
            ax.set_ylim3d(-50, 100)
            ax.set_zlim3d(0, 100)
            ax.set_xlabel("X-axis")
            ax.set_ylabel("Y-axis")
            ax.set_zlabel("Z-axis")
            ax.set_axisbelow(True)
            ax.plot(
                [0, 0, 0, 0, 40, 0, -40, 0,  40, 0, -40, 0],
                [60, 0, 60, 0, 20, 0,  20, 0,  20, 0, 20, 0],
                [40, 0, 75, 0, 40, 0,  40, 0,  75, 0, 75, 0],
                "o-",
                markerSize=3,
                markerFacecolor="orange",
                linewidth=0.3,
                color="blue"
            )
            x_points = _map(
                (inputs["left_x"], -1, 1, -40, 40))
            y_points = _map((inputs["left_y"], -1, 1, 0, 60))
            z_points = _map((inputs["right_y"], -1, 1, 0, 75))
            ax.plot(
                x_points, y_points, z_points,
                "o-",
                markerSize=2,
                markerFacecolor="orange",
                linewidth=1,
                color="red"
            )
            plt.pause(0.0000000000001)
        except KeyError as e:
            print("Roll")

    ax.set_xlim3d(-50, 50)
    ax.set_ylim3d(-50, 100)
    ax.set_zlim3d(0, 100)
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.set_zlabel("Z-axis")
    ax.set_axisbelow(True)
    plt.show()
