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
                    axis_data_1_z = (self._map(axis_data_1_z, -1, 1, 0, 30))

                    axis_data_2_z = self.axis_data[1]
                    axis_data_2_z = (self._map(axis_data_2_z, -1, 1, 40, 80))
                    print(axis_data_1_z, axis_data_2_z)
                  except KeyError as e:
                      axis_data_1_z = 0
                      print ("Roll Sticks!")
                  print("Sending Absolute Order")

                  self.sendLoad(bytearray([2, (axis_data_1_z), (axis_data_2_z)]))

                if self.button_data[3]:
                    print("Translate Z Mode")
                    axis_data_1_x: int = 0                    
                    try:
                        axis_data_1_x = self.axis_data[1]
                        axis_data_1_x = (self._map(axis_data_1_x, -1, 1, 0, 50))
                        print(axis_data_1_x)
                    except KeyError as e:
                        axis_data_1_x = 0
                        print ("Roll Sticks!")
                    print("Sending Absolute Order")
                    self.sendLoad(bytearray([1, axis_data_1_x]))

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

                
                if self.button_data[5]:
                  print ("Decrementing Speed")
                  data = self.getEquidistantPoints( (50, 40), (140, 90), 20 )
                  self.sendLoad(bytearray([12]))

            

                if self.button_data[12]:
                    print("Goodbye!")
                    exit(0)



if __name__ == "__main__":
    ps4 = PS4Controller()
    ps4.init()
    ps4.listen()