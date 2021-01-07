import socket
import os
import pprint
import pygame
import numpy as np
import copy
import glob
import time

class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = None
    button_data = None
    hat_data = None
    
    HOST = '192.168.0.248'  # The server's hostname or IP address
    PORT = 80               # The port used by the server 
    def init(self):
        """Initialize the joystick components"""
        
        pygame.init()
        pygame.joystick.init()
        self.axisMode = False
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
        self.HOST = '192.168.0.248'
        self.PORT = 80
        self.bounceMode = False
        self.currentX1 = 0
        self.currentY1 = 0
        self.currentZ1 = 0

        self.currentX2 = 0
        self.currentY2 = 0
        self.currentZ2 = 0

        self.currentX3 = 0
        self.currentY3 = 0
        self.currentZ3 = 0

        self.currentX4 = 0
        self.currentY4 = 0
        self.currentZ4 = 0

        self.absoluteControl = False



    def _map(self, x, in_min, in_max, out_min, out_max):
        return int((x-in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    def getEquidistantPoints(self,p1, p2, parts):
        return zip(np.linspace(p1[0], p2[0], parts+1),
               np.linspace(p1[1], p2[1], parts+1))
    
    def sendLoad(self, load:bytearray):
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                              s.connect((self.HOST, self.PORT))
                              s.sendall(load)

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
                    self.axis_data[event.axis] = round(event.value,2)
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
                
                if self.button_data[8]:
                  print("Sending to Home Position")
                  self.sendLoad(bytearray([3]))

                if self.button_data[11]:
                    print("Toggling Bounce Mode")
                    self.bounceMode = not self.bounceMode
                    print("Bounce Mode: " + str(self.bounceMode))
                    self.sendLoad(bytearray([1, self.bounceMode]))
                
                """
                    In Rotation Mode around Z:
                        X can go max to 30 and min to -30. 
                        Y has to be stagnant. 
                        Z can go max to 80 and min to 40.
                """

                if self.button_data[2]:
                  print("Rotation Mode")
                  axis_data_1_z: int = 0
                  try:
                    axis_data_1_z = self.axis_data[0]
                    axis_data_1_z = (self._map(axis_data_1_z, -1, 1, 0, 40))

                    axis_data_2_z = self.axis_data[1]
                    axis_data_2_z = (self._map(axis_data_2_z, -1, 1, 40, 100))
                    print(axis_data_1_z, axis_data_2_z)

                  except KeyError as e:
                      axis_data_1_z = 0
                      print ("Roll Sticks!")
                  print("Sending Absolute Order")
                  self.sendLoad(bytearray([2, (axis_data_1_z), (axis_data_2_z)]))

                if self.button_data[4]:
                  print("Rotation Mode")
                  data_points = list(self.getEquidistantPoints((10, 65), (155, 95), 200 ))  
                  point = self._map(self.axis_data[5],-1, 1, 0, 200  )
                  pointX = self._map(self.axis_data[2], -1,1, 0, 40)
                  pointZ = self._map(self.axis_data[1], -1, 1, 0, 200)

                  self.currentX1 = pointX
                  self.currentY1 = data_points[point ][0]
                  self.currentZ1 = data_points[point ][1]

                  self.currentX2 = pointX
                  self.currentY2 = data_points[point][0]
                  self.currentZ2 = data_points[point][1]

                  self.currentX3 = pointX
                  self.currentY3 = data_points[200 - pointZ][0]
                  self.currentZ3 = data_points[200 - pointZ][1]

                  self.currentX4 = pointX
                  self.currentY4 = data_points[200 - pointZ][0]
                  self.currentZ4 = data_points[200 - pointZ][1]


                if self.button_data[5]:
                    print("Translate Z Mode")

                    data_points = list(self.getEquidistantPoints((10, 65), (155, 95), 200 ))
                    
                    point = self._map(self.axis_data[5],-1, 1, 0, 200  )
                    

                    pointX = self._map(self.axis_data[0], -1,1, 0, 40)

                    pointY = self._map(self.axis_data[1], -1, 1, 0, 40)
                    self.currentX1 = 40 - pointX
                    self.currentY1 = data_points[point][0]
                    self.currentZ1 = data_points[point][1]

                    self.currentX2 = pointX
                    self.currentY2 = data_points[point][0]
                    self.currentZ2 = data_points[point][1]

                    self.currentX3 = pointX
                    self.currentY3 = data_points[point][0]
                    self.currentZ3 = data_points[point][1]

                    self.currentX4 = 40 - pointX
                    self.currentY4 = data_points[point][0]
                    self.currentZ4 = data_points[point][1]
                    
                    
                if self.button_data[0]: #Holding X
                  print("Holding X")
                  if self.hat_data[0][1] == 1:
                    self.sendLoad(bytearray([1]))
                    
                  
                  if self.hat_data[0][1] == -1:
                    self.sendLoad(bytearray([2]))
                    

                      
                            
                if self.button_data[1]: #Holding Y
                  print("Holding Y")
                  
                  if self.hat_data[0][1] == 1:
                    self.sendLoad(bytearray([3]))
                    
                  
                  if self.hat_data[0][1] == -1:
                    self.sendLoad(bytearray([4]))
                    
          
                if self.button_data[9]:
                  print ("Starting Animation")
                  data = self.getEquidistantPoints( (50, 40), (140, 90), 20 )
                  self.sendLoad(bytearray([10]))
                
                if self.button_data[4]:
                  print ("Incrementing Speed")
                  data = self.getEquidistantPoints( (50, 40), (140, 90), 20 )
                  self.sendLoad(bytearray([11]))

                if self.button_data[12]:
                    print("Goodbye!")
                    exit(0)

                if self.button_data[13]:
                  print("Marching")
                  
                  data_points = list(self.getEquidistantPoints((10, 65), (155, 95), 200 ))

                  limitedPoints = []
                  limitedPoints = data_points[10:100]
                  
                  
                  toggle = 1
                  for x in range((10)):
                    
                    toggle = not toggle 
                    self.currentX1 = 20
                    self.currentY1 = 65 if toggle else 60
                    self.currentZ1 = 40 

                    self.currentX2 = 20
                    self.currentY2 = 65 if toggle else 60
                    self.currentZ2 = 40
                    
                    self.currentX3 = 20
                    self.currentY3 = 60 if toggle else 65
                    self.currentZ3 = 40

                    self.currentX4 = 20 
                    self.currentY4 = 60 if toggle else 65
                    self.currentZ4 = 40

                    self.sendLoad((bytearray(
                      [1, 
                      int(self.currentX1), int(self.currentX2), int(self.currentX3), int(self.currentX4),
                      int(self.currentY1), int(self.currentY2), int(self.currentY3), int(self.currentY4),
                      int(self.currentZ1), int(self.currentZ2), int(self.currentZ3), int(self.currentZ4)
                      ])))
                    
                    time.sleep(0.1)
                    




                if not self.absoluteControl:
                  self.sendLoad((bytearray(
                    [1, 
                    int(self.currentX1), int(self.currentX2), int(self.currentX3), int(self.currentX4),
                    int(self.currentY1), int(self.currentY2), int(self.currentY3), int(self.currentY4),
                    int(self.currentZ1), int(self.currentZ2), int(self.currentZ3), int(self.currentZ4)
                    ])))
                


if __name__ == "__main__":
    ps4 = PS4Controller()
    ps4.init()
    ps4.listen()