import math
import numpy as np
import socket


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

    def up(self, leg: int) -> None:
        if leg == 1:
            self.leg_1.move(20, 60, 40)
        elif leg == 2:
            self.leg_2.move(20, 60, 40)
        elif leg == 3:
            self.leg_3.move(20, 60, 40)
        elif leg == 5:
            self.leg_4.move(20, 60, 40)
        return None

    def down(self, leg: int, increment) -> None:
        if leg == 1:
            self.leg_1.move(20, 45 + increment, 60 + increment)
        elif leg == 2:
            self.leg_2.move(20, 45 + increment, 60 + increment)
        elif leg == 3:
            self.leg_3.move(20, 45 + increment, 60 + increment)
        elif leg == 4:
            self.leg_4.move(20, 45 + increment, 60 + increment)

        return None

    def upFront(self, leg: int, ) -> None:
        if leg == 1:
            self.leg_1.move(40, 20, 40)
        elif leg == 2:
            self.leg_2.move(40, 20, 40)
        elif leg == 3:
            self.leg_3.move(40, 20, 40)
        elif leg == 4:
            self.leg_4.move(40, 20, 40)
        return None

    def downFront(self, leg: int) -> None:
        if leg == 1:
            self.leg_1.move(40, 20, 60)
        elif leg == 2:
            self.leg_2.move(40, 20, 60)
        elif leg == 3:
            self.leg_3.move(40, 20, 60)
        elif leg == 4:
            self.leg_4.move(40, 20, 60)
        return None

    def upBack(self, leg):
        if leg == 1:
            self.leg_1.move(self._map(-20, -30, 30, 0, 40), 20, 40)
        elif leg == 2:
            self.leg_2.move(self._map(-20, -30, 30, 0, 40), 20, 40)
        elif leg == 3:
            self.leg_3.move(self._map(-20, -30, 30, 0, 40), 20, 40)
        elif leg == 4:
            self.leg_4.move(self._map(-20, -30, 30, 0, 40), 20, 40)
        return None

    def downBack(self, leg):
        if leg == 1:
            self.leg_1.move(self._map(-20, -30, 30, 0, 40), 20, 60)
        elif leg == 2:
            self.leg_2.move(self._map(-20, -30, 30, 0, 40), 20, 60)
        elif leg == 3:
            self.leg_3.move(self._map(-20, -30, 30, 0, 40), 20, 60)
        elif leg == 4:
            self.leg_4.move(self._map(-20, -30, 30, 0, 40), 20, 60)
        return None


if __name__ == "__main__":
    robo: RobotModel = RobotModel("192.168.0.248", 80)
    robo.up(1)
    print(robo.leg_1.show())
    robo.down(1, 30)
    print(robo.leg_1.show())
    robo.downBack(1)
    print(robo.leg_1.show())
