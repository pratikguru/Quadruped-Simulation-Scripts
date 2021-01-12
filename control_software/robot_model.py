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
    def __init__(self, host: int, port: int = 80):

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

    def _map(self, x, in_min, in_max, out_min, out_max) -> int:
        return int((x-in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    def _getTrajectory(self, pt1: tuple, pt2: tuple, fine: int) -> list:
        return list(zip(np.linspace(pt1[0], pt2[0], fine+1),
                        np.linspace(pt1[1], pt2[1], fine+1)))

    def sendLoad(self, load: list) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(load)
            s.close()
        return None

    def reload(self):
        self.sendLoad(bytearray(
            [
                1,
                int(self.leg_1.x), int(self.leg_2.x), int(
                    self.leg_3.x), int(self.leg_4.x),
                int(self.leg_1.y), int(self.leg_2.y), int(
                    self.leg_3.y), int(self.leg_4.y),
                int(self.leg_1.z), int(self.leg_2.z), int(
                    self.leg_3.z), int(self.leg_4.z)
            ]
        ))

    def trotTraverse(self, direction):
        stepInterval: float = 0.08
        increment: int = 0

        loops: dict = {
            "cyc-1": {
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
            "cyc-2": {
                "1": {
                    "fn": self.upFront
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
            },
            "cyc-3": {
                "1": {
                    "fn": self.downFront
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
            },
            "cyc-4": {
                "1": {
                    "fn": self.downFront
                },
                "2": {
                    "fn": self.down,
                },
                "3": {
                    "fn": self.upFront
                },
                "4": {
                    "fn": self.down
                }
            },

            "cyc-4": {
                "1": {
                    "fn": self.downFront
                },
                "2": {
                    "fn": self.down,
                },
                "3": {
                    "fn": self.downBack
                },
                "4": {
                    "fn": self.down
                }
            },
            "cyc-5": {
                "1": {
                    "fn": self.downFront
                },
                "2": {
                    "fn": self.upFront,
                },
                "3": {
                    "fn": self.downBack
                },
                "4": {
                    "fn": self.down
                }
            },
            "cyc-6": {
                "1": {
                    "fn": self.downFront
                },
                "2": {
                    "fn": self.downFront,
                },
                "3": {
                    "fn": self.downBack
                },
                "4": {
                    "fn": self.down
                }
            },
            "cyc-6": {
                "1": {
                    "fn": self.downFront
                },
                "2": {
                    "fn": self.downFront,
                },
                "3": {
                    "fn": self.downBack
                },
                "4": {
                    "fn": self.upBack
                }
            },
            "cyc-6": {
                "1": {
                    "fn": self.downFront
                },
                "2": {
                    "fn": self.downFront,
                },
                "3": {
                    "fn": self.downBack
                },
                "4": {
                    "fn": self.downBack
                }
            }
        }

        for key, value in loops.items():
            for key2, value2 in value.items():
                for key3, value3 in value2.items():
                    try:
                        value3(int(key2))
                    except TypeError as e:
                        pass
            time.sleep(stepInterval)
            self.reload()

    def trotRotate(self, direction):
        stepInterval: float = 0.2
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
                    except TypeError as e:
                        pass
            time.sleep(stepInterval)
            self.reload()

    def rotate(self, axis_1, axis_2, axis_3, axis) -> None:
        data_points = self._getTrajectory((10, 65), (155, 95), 200)
        point_z = self._map(axis_1, - 1, 1, 0, 200)
        point_x = self._map(axis_2, -1, 1, 0, 40)
        point_3 = self._map(axis_3, -1, 1, 0, 200)

        if axis == "x":
            self.leg_1.y = data_points[200 - point_z][0]
            self.leg_1.z = data_points[200 - point_z][1]

            self.leg_3.y = data_points[point_3][0]
            self.leg_3.z = data_points[point_3][1]

        elif axis == "y":
            self.leg_1.y = data_points[point_3][0]
            self.leg_1.z = data_points[point_3][1]

            self.leg_3.y = data_points[200 - point_z][0]
            self.leg_3.z = data_points[200 - point_z][1]

        self.leg_1.x = point_x

        self.leg_2.x = point_x
        self.leg_2.y = data_points[point_3][0]
        self.leg_2.z = data_points[point_3][1]

        self.leg_3.x = point_x

        self.leg_4.x = point_x
        self.leg_4.y = data_points[200 - point_z][0]
        self.leg_4.z = data_points[200 - point_z][1]
        return None

    def translate(self, axis_1, axis_2, axis_3, axis) -> None:
        data_points = self._getTrajectory((10, 65), (155, 95), 200)
        point_1 = self._map(axis_3, -1, 1, 0, 200)
        point_2 = self._map(axis_1, -1, 1, 0, 40)
        point_3 = self._map(axis_2, -1, 1, 0, 40)

        if axis == "x":
            self.leg_1.x = 40 - point_2
            self.leg_3.x = point_2
        elif axis == "y":
            self.leg_1.x = point_2
            self.leg_3.x = 40 - point_2

        self.leg_1.y = data_points[point_1][0]
        self.leg_1.z = data_points[point_1][1]

        self.leg_2.x = point_2
        self.leg_2.y = data_points[point_1][0]
        self.leg_2.z = data_points[point_1][1]

        self.leg_3.y = data_points[point_1][0]
        self.leg_3.z = data_points[point_1][1]

        self.leg_4.x = 40 - point_2
        self.leg_4.y = data_points[point_1][0]
        self.leg_4.z = data_points[point_1][1]
        return None

    def up(self, leg: int) -> None:
        if leg == 1:
            self.leg_1.move(20, 60, 40)
        elif leg == 2:
            self.leg_2.move(20, 60, 40)
        elif leg == 3:
            self.leg_3.move(20, 60, 40)
        elif leg == 5:
            self.leg_4.move(20, 60, 40)
        else:
            print("not")
        return None

    def down(self, leg: int, increment=0) -> None:

        if leg == 1:
            self.leg_1.move(20, 45 + increment, 60 + self.increment)
        elif leg == 2:
            self.leg_2.move(20, 45 + increment, 60 + self.increment)
        elif leg == 3:
            self.leg_3.move(20, 45 + increment, 60 + self.increment)
        elif leg == 4:
            self.leg_4.move(20, 45 + increment, 60 + self.increment)

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
