"""
  Basic imports and defaults.
"""
from joystick_controller import *
import os
from pprint import pprint
import numpy as np
import math


from robot_model import *
"""
  Process related imports.
"""

if __name__ == "__main__":
    ps4: PS4Controller = PS4Controller()
    ps4.init()

    toggle_debug: bool = True
    translateMode: bool = False
    rotateMode: bool = False

    axis: str = "y"

    while True:
        robot: RobotModel = RobotModel("192.168.0.248", 80)

        os.system("clear")
        inputs: dict = (ps4.listen())
        print("Debug: " + str(toggle_debug))
        print("Translate Mode: " + str(translateMode))
        if translateMode:
            print("Axis: " + str(axis))

        print("Rotate Mode: " + str(rotateMode))
        if rotateMode:
            print("Axis: " + str(axis))

        if inputs["option"]:
            toggle_debug = not toggle_debug

        if toggle_debug:
            pprint(inputs)

        if inputs["home"]:
            print("Closing goodbye!")
            break

        if inputs["r1"]:
            print("Rotating")
            robot.trotRotate(direction=1)
            # robot.trotTraverse(direction=1)

        if inputs["r2"]:
            robot.trotTraverse(direction=1)

        if inputs["l2"]:
            robot.trotTraverse(direction=0)

        if inputs["l1"]:
            print("Rotating")
            robot.trotRotate(direction=0)

        if inputs["s"] == 1 and not inputs["o"] == 1:
            print("Toggling Translate Mode")
            translateMode = not translateMode

        if inputs["o"] == 1 and not inputs["s"] == 1:
            print("Toggling Rotate Mode")
            rotateMode = not rotateMode

        if inputs["x"]:
            print("testing move")

            robot.step(1)

        if rotateMode:
            if inputs["x"] == 1:
                axis = "x"
            elif inputs["t"] == 1:
                axis = "y"
            try:
                robot.rotate(inputs["left_y"], inputs["left_x"],
                             inputs["right_y"], axis=axis)
                print(robot.leg_1.show())
                print(robot.leg_2.show())
                print(robot.leg_3.show())
                print(robot.leg_4.show())
                robot.reload()
            except KeyError as e:
                print("Roll Sticks")

        if translateMode:
            if inputs["x"] == 1:
                axis = "x"
            elif inputs["t"] == 1:
                axis = "y"
            try:
                robot.translate(inputs['left_x'],
                                inputs['left_y'], inputs['right_y'], axis=axis)
                print(robot.leg_1.show())
                print(robot.leg_2.show())
                print(robot.leg_3.show())
                print(robot.leg_4.show())
                robot.reload()
            except KeyError as e:
                print("Roll Sticks")

        time.sleep(0.05)
