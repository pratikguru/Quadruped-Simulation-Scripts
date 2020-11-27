from numpy import interp 
import serial



serialObj = serial.Serial()
serialObj.timeout = 4
serialObj.baudrate= "115200"
serialObj.port = "/dev/cu.usbmodem14101"
serialObj.open()


serialObj.write((97))
serialObj.close()