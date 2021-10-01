import math
from person import Person
from pyax12.connection import Connection

class Turret:

    def __init__(self):
      
        self.IDx = 2
        self.IDy = 1
        self.SpeedX = 250
        self.SpeedY = 50
        self.MaxAngle = 20.0

        self.serial_connection = Connection(port="/dev/ttyS0", baudrate=1000000)

    def MoveTurretToPerson(self, person):
        
        theta = self.GetThetaAngle(person.x, person.z)
        rho = self.GetRhoAngle(person.y, person.z)

        if theta != None and rho != None:
            self.MoveTurretWithAngle(theta, rho)

    def MoveTurretWithAngle(self,theta, rho):

        rho = self.LimitRho(rho)

        if rho < -20.0:
            return

        self.serial_connection.goto(self.IDx, theta, speed=self.SpeedX, degrees=True)

        if rho > -20.0:
            self.serial_connection.goto(self.IDy, rho, speed=self.SpeedY, degrees=True)

    def LimitRho(self,rho):

        if rho == None:
            return 0

        if rho > self.MaxAngle:
            rho = self.MaxAngle

        if rho < -self.MaxAngle:
            rho = -self.MaxAngle

        return rho
    
    def GetAtan(self,oposite, adyacent):
        radian_angle = math.atan(oposite/adyacent)
        degree_angle = radian_angle*180/math.pi
        return round(degree_angle,1)

    def GetThetaAngle(self,x,z):
        if z != 0.0:
            z = z - 100
            x = x * -1.0
            return self.GetAtan(x, z)

    def GetRhoAngle(self,y,z):
        if z != 0.0:
            z = z - 100
            y = y + 10
            return self.GetAtan(y, z)


        
        