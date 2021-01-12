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

    HOST = '192.168.18.210'  # The server's hostname or IP address
    PORT = 80               # The port used by the server

    def init(self):
        """Initialize the joystick components"""

        pygame.init()
        pygame.joystick.init()
        self.axisMode = False
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
        self.HOST = '192.168.18.210'
        self.PORT = 80
        self.bounceMode = False
        self.currentX1 = 20
        self.currentY1 = 60
        self.currentZ1 = 40

        self.currentX2 = 20
        self.currentY2 = 60
        self.currentZ2 = 40

        self.currentX3 = 20
        self.currentY3 = 60
        self.currentZ3 = 40

        self.currentX4 = 20
        self.currentY4 = 60
        self.currentZ4 = 40

        self.absoluteControl = True
        self.live = False

    def _map(self, x, in_min, in_max, out_min, out_max):
        return int((x-in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    def getEquidistantPoints(self, p1, p2, parts):
        return zip(np.linspace(p1[0], p2[0], parts+1),
                   np.linspace(p1[1], p2[1], parts+1))

    def handleRotate(self,
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

    def sendLoad(self, load: bytearray):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            s.sendall(load)
            s.close()

    def upControlled(self, leg, angle):
        if leg == 1:
            self.currentX1 = angle
            self.currentY1 = 60
            self.currentZ1 = 40
        elif leg == 2:
            self.currentX2 = angle
            self.currentY2 = 60
            self.currentZ2 = 40
        elif leg == 3:
            self.currentX3 = angle
            self.currentY3 = 60
            self.currentZ3 = 40
        elif leg == 4:
            self.currentX4 = angle
            self.currentY4 = 60
            self.currentZ4 = 40

    def up(self, leg):
        if leg == 1:
            self.currentX1 = 20
            self.currentY1 = 60
            self.currentZ1 = 40
        elif leg == 2:
            self.currentX2 = 20
            self.currentY2 = 60
            self.currentZ2 = 40
        elif leg == 3:
            self.currentX3 = 20
            self.currentY3 = 60
            self.currentZ3 = 40
        elif leg == 4:
            self.currentX4 = 20
            self.currentY4 = 60
            self.currentZ4 = 40

    def down(self, leg):
        if leg == 1:
            self.currentX1 = 20
            self.currentY1 = 60
            self.currentZ1 = 75
        elif leg == 2:
            self.currentX2 = 20
            self.currentY2 = 60
            self.currentZ2 = 75
        elif leg == 3:
            self.currentX3 = 20
            self.currentY3 = 60
            self.currentZ3 = 75
        elif leg == 4:
            self.currentX4 = 20
            self.currentY4 = 60
            self.currentZ4 = 75

    def upFront(self, leg):
        if leg == 1:
            self.currentX1 = 40
            self.currentY1 = 20
            self.currentZ1 = 40
        elif leg == 2:
            self.currentX2 = 40
            self.currentY2 = 20
            self.currentZ2 = 40
        elif leg == 3:
            self.currentX3 = 40
            self.currentY3 = 20
            self.currentZ3 = 40
        elif leg == 4:
            self.currentX4 = 40
            self.currentY4 = 20
            self.currentZ4 = 40

    def downFront(self, leg):
        if leg == 1:
            self.currentX1 = 40
            self.currentY1 = 20
            self.currentZ1 = 60
        elif leg == 2:
            self.currentX2 = 40
            self.currentY2 = 20
            self.currentZ2 = 60
        elif leg == 3:
            self.currentX3 = 40
            self.currentY3 = 20
            self.currentZ3 = 60
        elif leg == 4:
            self.currentX4 = 40
            self.currentY4 = 20
            self.currentZ4 = 60

    def upBack(self, leg):
        if leg == 1:
            self.currentX1 = self._map(-20, -30, 30, 0, 40)
            self.currentY1 = 20
            self.currentZ1 = 40
        elif leg == 2:
            self.currentX2 = self._map(-20, -30, 30, 0, 40)
            self.currentY2 = 20
            self.currentZ2 = 40
        elif leg == 3:
            self.currentX3 = self._map(-20, -30, 30, 0, 40)
            self.currentY3 = 20
            self.currentZ3 = 40
        elif leg == 4:
            self.currentX4 = self._map(-20, -30, 30, 0, 40)
            self.currentY4 = 20
            self.currentZ4 = 40

    def downBack(self, leg):
        if leg == 1:
            self.currentX1 = self._map(-30, -30, 30, 0, 40)
            self.currentY1 = 20
            self.currentZ1 = 60
        elif leg == 2:
            self.currentX2 = self._map(-30, -30, 30, 0, 40)
            self.currentY2 = 20
            self.currentZ2 = 60
        elif leg == 3:
            self.currentX3 = self._map(-30, -30, 30, 0, 40)
            self.currentY3 = 20
            self.currentZ3 = 60
        elif leg == 4:
            self.currentX4 = self._map(-30, -30, 30, 0, 40)
            self.currentY4 = 20
            self.currentZ4 = 60

    def stanceUp(self, leg):
        if leg == 1:
            self.currentX1 = 10
            self.currentY1 = 60
            self.currentZ1 = 40
        elif leg == 2:
            self.currentX2 = 30
            self.currentY2 = 60
            self.currentZ2 = 40
        elif leg == 3:
            self.currentX3 = 10
            self.currentY3 = 60
            self.currentZ3 = 40
        elif leg == 4:
            self.currentX4 = 30
            self.currentY4 = 60
            self.currentZ4 = 40

    def stanceDown(self, leg, increment):
        if leg == 1:
            self.currentX1 = 10
            self.currentY1 = 45 + increment
            self.currentZ1 = 60 + increment
        elif leg == 2:
            self.currentX2 = 30
            self.currentY2 = 45 + increment
            self.currentZ2 = 60 + increment
        elif leg == 3:
            self.currentX3 = 10
            self.currentY3 = 45 + increment
            self.currentZ3 = 40 + increment
        elif leg == 4:
            self.currentX4 = 30
            self.currentY4 = 45 + increment
            self.currentZ4 = 60 + increment

    def stanceDownSide(self, leg, increment, rotation):
        if leg == 1:
            self.currentX1 = 10 + rotation
            self.currentY1 = 45 + increment
            self.currentZ1 = 60 + increment
        elif leg == 2:
            self.currentX2 = 30 - rotation
            self.currentY2 = 45 + increment
            self.currentZ2 = 60 + increment
        elif leg == 3:
            self.currentX3 = 10 + rotation
            self.currentY3 = 45 + increment
            self.currentZ3 = 40 + increment
        elif leg == 4:
            self.currentX4 = 30 - rotation
            self.currentY4 = 45 + increment
            self.currentZ4 = 60 + increment

    def stanceUpSide(self, leg, rotation):
        if leg == 1:
            self.currentX1 = 10 + rotation
            self.currentY1 = 60
            self.currentZ1 = 40
        elif leg == 2:
            self.currentX2 = 30 - rotation
            self.currentY2 = 60
            self.currentZ2 = 40
        elif leg == 3:
            self.currentX3 = 10 + rotation
            self.currentY3 = 60
            self.currentZ3 = 40
        elif leg == 4:
            self.currentX4 = 30 - rotation
            self.currentY4 = 60
            self.currentZ4 = 40

    def reload(self):
        self.sendLoad((bytearray(
                      [1,
                       int(self.currentX1), int(self.currentX2), int(
                           self.currentX3), int(self.currentX4),
                       int(self.currentY1), int(self.currentY2), int(
                           self.currentY3), int(self.currentY4),
                       int(self.currentZ1), int(self.currentZ2), int(
                           self.currentZ3), int(self.currentZ4)
                       ])))

    def step(self, leg):
        step_time = 0.2
        step_interval = 0.08
        self.upBack(leg)
        self.reload()
        time.sleep(step_time)
        self.downBack(leg)
        self.reload()
        time.sleep(step_time * 5)
        self.downFront(leg)
        self.reload()
        time.sleep(step_time)
        self.upFront(leg)
        self.reload()

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

        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[event.axis] = round(event.value, 2)
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.button_data[event.button] = True
                elif event.type == pygame.JOYBUTTONUP:
                    self.button_data[event.button] = False
                elif event.type == pygame.JOYHATMOTION:
                    self.hat_data[event.hat] = event.value

                # Insert your code on what you would like to happen for each event here!
                # In the current setup, I have the state simply printing out to the screen.

                os.system('clear')
                pprint.pprint(self.button_data)
                pprint.pprint(self.axis_data)
                pprint.pprint(self.hat_data)

                print(self.currentX1, self.currentY1, self.currentZ1)

                if self.button_data[6]:
                    print("Forward")

                if self.hat_data[0][1] == 1:
                    stepInterval = 0.1
                    self.down(1)
                    self.down(2)
                    self.down(3)
                    self.down(4)
                    self.reload()
                    time.sleep(stepInterval)

                    self.up(1)
                    self.up(2)
                    self.up(3)
                    self.up(4)
                    self.reload()
                    time.sleep(stepInterval)

                    self.upBack(1)
                    self.upBack(3)
                    self.down(4)
                    self.down(2)
                    self.reload()
                    time.sleep(stepInterval)

                    self.upBack(1)
                    self.upBack(3)
                    self.up(4)
                    self.up(2)
                    self.reload()
                    time.sleep(stepInterval)

                    self.downBack(1)
                    self.downBack(3)
                    self.down(4)
                    self.down(2)
                    self.reload()
                    time.sleep(stepInterval)

                    self.downBack(1)
                    self.downBack(3)
                    self.upBack(4)
                    self.upBack(2)
                    self.reload()
                    time.sleep(stepInterval)

                    self.downBack(1)
                    self.downBack(3)
                    self.downBack(4)
                    self.downBack(2)
                    self.reload()
                    time.sleep(stepInterval)

                    self.down(1)
                    self.down(2)
                    self.down(3)
                    self.down(4)
                    self.reload()

                if self.hat_data[0][1] == -1:
                    stepInterval = 0.1
                    print("Right")
                    self.down(1)
                    self.down(2)
                    self.down(3)
                    self.down(4)
                    self.reload()
                    time.sleep(stepInterval)

                    self.up(1)
                    self.up(2)
                    self.up(3)
                    self.up(4)
                    self.reload()
                    time.sleep(stepInterval)

                    self.upFront(1)
                    self.upFront(3)
                    self.down(4)
                    self.down(2)
                    self.reload()
                    time.sleep(stepInterval)

                    self.upFront(1)
                    self.upFront(3)
                    self.up(4)
                    self.up(2)
                    self.reload()
                    time.sleep(stepInterval)

                    self.downFront(1)
                    self.downFront(3)
                    self.down(4)
                    self.down(2)
                    self.reload()
                    time.sleep(stepInterval)

                    self.downFront(1)
                    self.downFront(3)
                    self.upFront(4)
                    self.upFront(2)
                    self.reload()
                    time.sleep(stepInterval)

                    self.downFront(1)
                    self.downFront(3)
                    self.downFront(4)
                    self.downFront(2)
                    self.reload()
                    time.sleep(stepInterval)

                    self.down(1)
                    self.down(2)
                    self.down(3)
                    self.down(4)
                    self.reload()

                if self.hat_data[0][0] == -1:
                    baseY = 45

                    baseZ = 60

                    stepIncrement = -15
                    stepInterval = 0.2

                    hipMin = 10
                    hipMax = 25

                    self.up(1)
                    self.up(2)
                    self.up(3)
                    self.up(4)
                    self.reload()
                    time.sleep(stepInterval)

                    self.down(2)
                    self.down(3)
                    self.down(4)
                    self.downBack(1)
                    self.reload()

                    time.sleep(stepInterval)
                    self.up(2)
                    self.up(3)
                    self.up(4)
                    self.upBack(1)
                    self.reload()

                    # set 2

                    time.sleep(stepInterval)
                    self.down(2)
                    self.down(4)
                    self.downBack(3)
                    self.downBack(1)
                    self.reload()

                    time.sleep(stepInterval)
                    self.up(2)
                    self.up(4)
                    self.upBack(3)
                    self.upBack(1)
                    self.reload()

                    time.sleep(stepInterval)
                    self.down(2)
                    self.downBack(4)
                    self.downBack(3)
                    self.downBack(1)
                    self.reload()

                    # set 3
                    time.sleep(stepInterval)
                    self.up(2)
                    self.upBack(4)
                    self.upBack(3)
                    self.upBack(1)
                    self.reload()

                    time.sleep(stepInterval)
                    self.downBack(2)
                    self.downBack(4)
                    self.downBack(3)
                    self.downBack(1)
                    self.reload()

                    time.sleep(stepInterval)

                    self.up(1)
                    self.up(2)
                    self.up(3)
                    self.up(4)
                    self.reload()

                if self.button_data[1]:
                    print("Stepping")

                    baseY = 30
                    baseZ = 45

                    stepIncrement = 0
                    stepInterval = 0.2

                    hipMin = 5
                    hipMax = 35
                    # Reaching top
                    self.currentX1 = 20
                    self.currentY1 = 60
                    self.currentZ1 = 40
                    self.reload()

                    # Reaching Left
                    time.sleep(0.3)
                    self.currentX1 = hipMax
                    self.currentY1 = baseY + stepIncrement
                    self.currentZ1 = baseZ + stepIncrement
                    self.reload()

                    # Reaching Right
                    time.sleep(0.3)
                    self.currentX1 = hipMin
                    self.currentY1 = baseY + stepIncrement
                    self.currentZ1 = baseZ + stepIncrement
                    self.reload()

                if self.hat_data[0][0] == 1:
                    print("high stepping")
                    baseY = 45
                    baseZ = 60

                    stepIncrement = -15
                    stepInterval = 0.2

                    hipMin = 10
                    hipMax = 25

                    self.up(1)
                    self.up(2)
                    self.up(3)
                    self.up(4)
                    self.reload()
                    time.sleep(stepInterval)

                    self.down(2)
                    self.down(3)
                    self.down(4)
                    self.downFront(1)
                    self.reload()

                    time.sleep(stepInterval)
                    self.up(2)
                    self.up(3)
                    self.up(4)
                    self.upFront(1)
                    self.reload()

                    # set 2

                    time.sleep(stepInterval)
                    self.down(2)
                    self.down(4)
                    self.downFront(3)
                    self.downFront(1)
                    self.reload()

                    time.sleep(stepInterval)
                    self.up(2)
                    self.up(4)
                    self.upFront(3)
                    self.upFront(1)
                    self.reload()

                    time.sleep(stepInterval)
                    self.down(2)
                    self.downFront(4)
                    self.downFront(3)
                    self.downFront(1)
                    self.reload()

                    # set 3
                    time.sleep(stepInterval)
                    self.up(2)
                    self.upFront(4)
                    self.upFront(3)
                    self.upFront(1)
                    self.reload()

                    time.sleep(stepInterval)
                    self.downFront(2)
                    self.downFront(4)
                    self.downFront(3)
                    self.downFront(1)
                    self.reload()

                    time.sleep(stepInterval)

                    self.up(1)
                    self.up(2)
                    self.up(3)
                    self.up(4)
                    self.reload()

                if self.button_data[12]:
                    print("Goodbye!")
                    exit(0)

                if self.button_data[3]:
                    print("Body Up")
                    data = list(self.getEquidistantPoints(
                        (60, 40), (50, 60), 100))

                    points = self._map(self.axis_data[1], -1, 1, 0, 100)
                    pointsX = self._map(self.axis_data[2], -1, 1, 0, 40)

                    self.currentX1 = pointsX
                    self.currentY1 = data[points][0]
                    self.currentZ1 = data[points][1]

                    self.currentX2 = pointsX
                    self.currentY2 = data[points][0]
                    self.currentZ2 = data[points][1]

                    self.currentX3 = pointsX
                    self.currentY3 = data[points][0]
                    self.currentZ3 = data[points][1]

                    self.currentX4 = pointsX
                    self.currentY4 = data[points][0]
                    self.currentZ4 = data[points][1]
                    self.reload()

                if self.live:
                    points = list(self.getEquidistantPoints(
                        (60, 40), (45, 60), 100))
                    try:
                        cursor = self._map(self.axis_data[1], -1, 1, 0, 100)
                        print(points)
                        self.currentX1 = self._map(
                            self.axis_data[2], -1, 1, 5, 35)
                        self.currentY1 = points[cursor][0]
                        self.currentZ1 = points[cursor][1]

                        self.currentX2 = self._map(
                            self.axis_data[2], -1, 1, 5, 35)
                        self.currentY2 = points[cursor][0]
                        self.currentZ2 = points[cursor][1]

                        self.currentX3 = self._map(
                            self.axis_data[2], -1, 1, 5, 35)
                        self.currentY3 = points[cursor][0]
                        self.currentZ3 = points[cursor][1]

                        self.currentX4 = self._map(
                            self.axis_data[2], -1, 1, 5, 35)
                        self.currentY4 = points[cursor][0]
                        self.currentZ4 = points[cursor][1]
                        self.reload()
                    except KeyError as e:
                        print("Roll Sticks")


if __name__ == "__main__":
    ps4 = PS4Controller()
    ps4.init()
    ps4.listen()


#   0, 60, 40 - up
#   0, 50, 60 - down

#   10, 50, 40 - front up
#   10, 50, 60 - font down

#   -10, 50, 50 - back down
#   -10, 50, 40, - back up

#     void up(int leg) {
#   getIk(0, 60, 40, leg);
# }

# void down(int leg) {
#   getIk(0, 50, 60, leg);
# }

# void frontUp(int leg) {
#   getIk(10, 50, 40, leg);
# }

# void frontDown(int leg) {

#   getIk(10, 50, 50, leg);
# }

# void backDown(int leg) {
#   getIk(-10, 50, 50, leg);
# }

# void backUp(int leg) {
#   getIk(-10, 50, 40, leg);
# }
