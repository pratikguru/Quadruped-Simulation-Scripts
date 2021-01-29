import math
import numpy as np
import socket
import time

from pprint import pprint


class Leg:
    def __init__(self, x: float, y: float, z: float, name: str = "leg"):
        self.name: str = name
        self.x: float = x
        self.y: float = y
        self.z: float = z

    def move(self, x: float, y: float, z: float) -> None:
        self.x: float = x
        self.y: float = y
        self.z: float = z
        return None

    def show(self) -> str:
        return "X:" + str(self.x) + " \tY:" + str(self.y) + "\tZ:" + str(self.z) + "\t" + str(self.name)


class RobotModel:
    def __init__(self, host: int, port: int = 80, activate: bool = False):

        # Connecting variables.
        self.host: str = host
        self.port: int = port

        # Leg variable setup.
        self.leg_1: Leg = Leg(x=20, y=60, z=40, name="leg-1")
        self.leg_2: Leg = Leg(x=20, y=60, z=40, name="leg-2")
        self.leg_3: Leg = Leg(x=20, y=60, z=40, name="leg-3")
        self.leg_4: Leg = Leg(x=20, y=60, z=40, name="leg-4")

        self.showOffMode: bool = False
        self.increment: int = 15
        self.activate: bool = activate

        self.previousPayload = []
        self.newPayload = []

    def _map(self, x, in_min, in_max, out_min, out_max) -> int:
        return int((x-in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    def _getTrajectory(self, pt1: tuple, pt2: tuple, fine: int) -> list:
        return list(zip(np.linspace(pt1[0], pt2[0], fine+1),
                        np.linspace(pt1[1], pt2[1], fine+1)))

    def _smooth(self, value: float, smooth: int) -> int:
        return sum([x for x in range(0, smooth)]) / smooth

    def sendLoad(self, load: list) -> None:
        if self.previousPayload == self.newPayload:
            print("Old State")
        else:

            if self.activate:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((self.host, self.port))
                    s.sendall(load)
                    s.close()
                return None
            else:
                return None
        self.previousPayload = load

    def restart(self):
        print("Restarting Robot")
        self.sendLoad(load=bytearray([9]))

    def reload(self):
        self.newPayload = [
            2,
            int(self.leg_1.x), int(self.leg_2.x), int(
                self.leg_3.x), int(self.leg_4.x),
            int(self.leg_1.y), int(self.leg_2.y), int(
                self.leg_3.y), int(self.leg_4.y),
            int(self.leg_1.z), int(self.leg_2.z), int(
                self.leg_3.z), int(self.leg_4.z)
        ]
        # self.sendLoad(bytearray(
        #     self.newPayload
        # ))

    def trotTraverse(self, direction):
        stepInterval: float = 0.3

        self.downBack(1)
        self.downBack(3)
        self.reload()

    def trotRotate(self, direction):
        stepInterval: float = 0.1
        increment: int = 0

        loops: dict = {
            "cycle-1": {
                "1": {
                    "fn": self.down,
                    "args": increment
                },
                "2": {
                    "fn": self.down,
                    "args": increment
                },
                "3": {
                    "fn": self.down,
                    "args": increment
                },
                "4": {
                    "fn": self.down,
                    "args": increment
                }
            },
            "cycle-2": {
                "1": {
                    "fn": self.upFront if direction else self.upBack
                },
                "2": {
                    "fn": self.down
                },
                "3": {
                    "fn": self.upFront if direction else self.upBack
                },
                "4": {
                    "fn": self.down
                },
            },
            "cycle-3": {
                "1": {
                    "fn": self.downFront if direction else self.downBack
                },
                "2": {
                    "fn": self.down
                },
                "3": {
                    "fn": self.downFront if direction else self.downBack
                },
                "4": {
                    "fn": self.down
                }
            },
            "cycle-4": {
                "1": {
                    "fn": self.downFront if direction else self.downBack,
                },
                "2": {
                    "fn": self.upFront if direction else self.upBack,
                },
                "3": {
                    "fn": self.downFront if direction else self.downBack
                },
                "4": {
                    "fn": self.upFront if direction else self.upBack
                }
            },
            "cycle-5": {
                "1": {
                    "fn": self.downFront if direction else self.downBack,
                },
                "2": {
                    "fn": self.downFront if direction else self.downBack,
                },
                "3": {
                    "fn": self.downFront if direction else self.downBack
                },
                "4": {
                    "fn": self.downFront if direction else self.downBack
                }
            },
            "cycle-6": {
                "1": {
                    "fn": self.down,
                },
                "2": {
                    "fn": self.down,
                },
                "3": {
                    "fn": self.down
                },
                "4": {
                    "fn": self.down
                }
            }
        }

        for key, value in loops.items():
            for key2, value2 in value.items():
                for key3, value3 in value2.items():

                    try:
                        value3(int(key2))
                    except TypeError:
                        pass
            time.sleep(stepInterval)
            self.reload()

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

    def rotate(self, axis_1, axis_2, axis_3, axis) -> None:

        precision: int = 500
        data_points = self._getTrajectory((10, 65), (155, 95), precision)
        rotation_precision: int = 40
        point_z = self._map(axis_1, - 1, 1, 0, precision)
        point_x = self._map(axis_2, -1, 1, 0, rotation_precision)
        point_3 = self._map(axis_3, -1, 1, 0, precision)

        if axis == "x":
            self.leg_1.y = data_points[precision - point_z][0]
            self.leg_1.z = data_points[precision - point_z][1]

            self.leg_3.y = data_points[point_3][0]
            self.leg_3.z = data_points[point_3][1]

        elif axis == "y":
            self.leg_1.y = data_points[point_3][0]
            self.leg_1.z = data_points[point_3][1]

            self.leg_3.y = data_points[precision - point_z][0]
            self.leg_3.z = data_points[precision - point_z][1]

        self.leg_1.x = point_x

        self.leg_2.x = point_x
        self.leg_2.y = data_points[point_3][0]
        self.leg_2.z = data_points[point_3][1]

        self.leg_3.x = point_x

        self.leg_4.x = point_x
        self.leg_4.y = data_points[precision - point_z][0]
        self.leg_4.z = data_points[precision - point_z][1]
        return None

    def translate(self, axis_1, axis_2, axis_3, axis) -> None:
        precision: int = 1000
        rotation_precision: int = 40
        data_points = self._getTrajectory((10, 65), (155, 95), precision)
        point_1 = self._map(axis_3, -1, 1, 0, precision)
        point_2 = self._map(
            self._map(axis_1, -1, 1, 0, precision), 0, precision, 0, rotation_precision)

        print("Point 1: " + str(point_1))
        print("data_points: " + str(data_points[point_1]))

        if axis == "x":
            self.leg_1.x = rotation_precision - point_2
            self.leg_3.x = point_2
        elif axis == "y":
            self.leg_1.x = point_2
            self.leg_3.x = rotation_precision - point_2

        self.leg_1.y = data_points[point_1][0]
        self.leg_1.z = data_points[point_1][1]

        self.leg_2.x = point_2
        self.leg_2.y = data_points[point_1][0]
        self.leg_2.z = data_points[point_1][1]

        self.leg_3.y = data_points[point_1][0]
        self.leg_3.z = data_points[point_1][1]

        self.leg_4.x = rotation_precision - point_2
        self.leg_4.y = data_points[point_1][0]
        self.leg_4.z = data_points[point_1][1]
        return None

    def step(self, leg):

        self.up(leg)
        self.reload()
        time.sleep(0.2)
        self.shortDownFront(leg)
        self.reload()
        time.sleep(0.2)
        self.shortDownBack(leg)
        self.reload()
        time.sleep(0.2)
        self.up(leg)
        self.reload()

    def up(self, leg: int) -> None:
        if leg == 1:
            self.leg_1.move(20, 60, 45)
        elif leg == 2:
            self.leg_2.move(20, 60, 45)
        elif leg == 3:
            self.leg_3.move(20, 60, 45)
        elif leg == 4:
            self.leg_4.move(20, 60, 45)

        return None

    def down(self, leg: int, increment=0) -> None:

        if leg == 1:
            self.leg_1.move(20, 45 + self.increment, 60 + self.increment)
        elif leg == 2:
            self.leg_2.move(20, 45 + self.increment, 60 + self.increment)
        elif leg == 3:
            self.leg_3.move(20, 45 + self.increment, 60 + self.increment)
        elif leg == 4:
            self.leg_4.move(20, 45 + self.increment, 60 + self.increment)

        return None

    def upFront(self, leg: int, ) -> None:
        turn: int = 40
        if leg == 1:
            self.leg_1.move(turn, 20, 40)
        elif leg == 2:
            self.leg_2.move(turn, 20, 40)
        elif leg == 3:
            self.leg_3.move(turn, 20, 40)
        elif leg == 4:
            self.leg_4.move(turn, 20, 40)
        return None

    def downFront(self, leg: int) -> None:
        turn: int = 40
        if leg == 1:
            self.leg_1.move(turn, 20, 60 + self.increment)
        elif leg == 2:
            self.leg_2.move(turn, 20, 60 + self.increment)
        elif leg == 3:
            self.leg_3.move(turn, 20, 60 + self.increment)
        elif leg == 4:
            self.leg_4.move(turn, 20, 60 + self.increment)
        return None

    def upBack(self, leg):
        turn: int = 0
        if leg == 1:
            self.leg_1.move(turn, 20, 40)
        elif leg == 2:
            self.leg_2.move(turn, 20, 40)
        elif leg == 3:
            self.leg_3.move(turn, 20, 40)
        elif leg == 4:
            self.leg_4.move(turn, 20, 40)
        return None

    def downBack(self, leg):
        turn: int = 0
        if leg == 1:
            self.leg_1.move(turn,
                            20, 60 + self.increment)
        elif leg == 2:
            self.leg_2.move(turn,
                            20, 60 + self.increment)
        elif leg == 3:
            self.leg_3.move(turn,
                            20, 60 + self.increment)
        elif leg == 4:
            self.leg_4.move(turn,
                            20, 60 + self.increment)
        return None

    def shortDownFront(self, leg):
        turn = 30
        if leg == 1:
            self.leg_1.move(turn,
                            45 + self.increment, 60 + self.increment)
        elif leg == 2:
            self.leg_2.move(turn,
                            45 + self.increment, 60 + self.increment)
        elif leg == 3:
            self.leg_3.move(turn,
                            45 + self.increment, 60 + self.increment)
        elif leg == 4:
            self.leg_4.move(turn,
                            45 + self.increment, 60 + self.increment)

    def shortDownBack(self, leg):
        turn = 10
        if leg == 1:
            self.leg_1.move(turn,
                            45 + self.increment, 60 + self.increment)
        elif leg == 2:
            self.leg_2.move(turn,
                            45 + self.increment, 60 + self.increment)
        elif leg == 3:
            self.leg_3.move(turn,
                            45 + self.increment, 60 + self.increment)
        elif leg == 4:
            self.leg_4.move(turn,
                            45 + self.increment, 60 + self.increment)

    def smoother(self, y, box_pts):
        box = np.ones(box_pts)/box_pts
        y_smooth = np.convolve(y, box, mode='same')
        return y_smooth


if __name__ == "__main__":
    robo: RobotModel = RobotModel("192.168.0.248", 80)
    robo.up(1)
    print(robo.leg_1.show())
    robo.down(1, 30)
    print(robo.leg_1.show())
    robo.downBack(1)
    print(robo.leg_1.show())

    robo.translate(0, 200, 300)
    print(robo.leg_1.show())
    print(robo.leg_2.show())
    print(robo.leg_3.show())
    print(robo.leg_4.show())
