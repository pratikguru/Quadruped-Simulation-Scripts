"""
  Basic imports and defaults.
"""
from joystick_controller import *
import os
from pprint import pprint
import numpy as np
import math

"""
  Process related imports.
"""

if __name__ == "__main__":
    ps4: PS4Controller = PS4Controller()
    ps4.init()

    toggle_debug: bool = True

    while True:
        os.system("clear")
        inputs: dict = (ps4.listen())
        print("Debug: " + str(toggle_debug))

        if inputs["option"]:
            toggle_debug = not toggle_debug

        if toggle_debug:
            pprint(inputs)

        if inputs["home"]:
            print("Closing goodbye!")
            break
        time.sleep(0.05)
