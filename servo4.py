from pyax12.connection import Connection
import time

# Connect to the serial port
serial_connection = Connection(port="/dev/ttyS0", baudrate=1000000)

IDx = 2
IDy = 1
SpeedX = 150
SpeedY = 50
MaxAngle = 20

time.sleep(1)

def LimitRho(rho):

    if rho > MaxAngle:
        rho = MaxAngle

    if rho < -MaxAngle:
        rho = -MaxAngle

    return rho
    

def MoveTurret(theta, rho):

    rho = LimitRho(rho)
    serial_connection.goto(IDx, theta, speed=SpeedX, degrees=True)
    serial_connection.goto(IDy, rho, speed=SpeedY, degrees=True)
    time.sleep(0.05)


MoveTurret(0,0)


# Close the serial connection
serial_connection.close()

