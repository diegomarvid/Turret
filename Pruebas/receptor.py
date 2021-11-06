# from pyax12.connection import Connection
# import time

# # Connect to the serial port
# serial_connection = Connection(port="/dev/ttyAMA0", baudrate=1000000)

# dynamixel_id = 2

# # Ping the third dynamixel unit
# serial_connection.goto(dynamixel_id, 15, speed=200, degrees=True)
# time.sleep(1)    # Wait 1 second

# # Close the serial connection
# serial_connection.close()

# import serial
# import time
# import RPi.GPIO as GPIO

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(18, GPIO.OUT)

# port = serial.Serial("/dev/serial0", baudrate=1000000, timeout=3.0)


# while True:
#         GPIO.output(18, GPIO.HIGH)
#         port.write(bytearray.fromhex("FF FF 02 05 03 1E 32 03 A3"))
#         time.sleep(0.1)
#         print("hola")
#         GPIO.output(18, GPIO.LOW)
#         time.sleep(1)

#         GPIO.output(18,GPIO.HIGH)
#         port.write(bytearray.fromhex("FF FF 02 05 03 1E CD 00 0b"))
#         time.sleep(0.1)
#         GPIO.output(18,GPIO.LOW)
#         time.sleep(1)

import serial 
import time 
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) 
GPIO.setup(18, GPIO.OUT)

port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3.0)
print(port)


while True: 
	x=port.readline()
	print(x)
    # GPIO.output(18, GPIO.HIGH) 
    # port.write(bytearray.fromhex("FF FF 01 05 03 1E 32 03 A3")) 
    # time.sleep(0.1) 
    # GPIO.output(18, GPIO.LOW) 
    # time.sleep(3)

    # GPIO.output(18,GPIO.HIGH) 
    # port.write(bytearray.fromhex("FF FF 01 05 03 1E CD 00 0b")) 
    # time.sleep(0.1) 
    # GPIO.output(18,GPIO.LOW) 
    # time.sleep(3)