import socket
import os
import pprint
import pygame
import numpy as np
import copy
import glob
import time

import math


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


if __name__ == "__main__":
    ps4 = PS4Controller()
    ps4.init()
    while True:
        os.system("clear")
        pprint.pprint(ps4.listen())
