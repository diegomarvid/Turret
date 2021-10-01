import RPi.GPIO as GPIO
import time
import math

THETA_MIN_DUTY = 2.75 #0.55ms
THETA_MAX_DUTY = 12.5 #2.5ms
THETA_ANGLE_RANGE = 180.0

x_0 = 2.75
x_180 = 12.5
x_m = (2.75 + x_180) / 2.0

slope = (x_180 - x_0) / 180
offset = x_m

THETA_SLOPE = (THETA_MAX_DUTY-THETA_MIN_DUTY)/THETA_ANGLE_RANGE
THETA_OFFSET = (THETA_MAX_DUTY+THETA_MIN_DUTY)/2.0

#THETA_SLOPE = (7.5 - 2.7) / 90

#THETA_OFFSET = 7.5

RHO_MIN_DUTY = 2.4
RHO_MAX_DUTY = 12.1
RHO_ANGLE_RANGE = 180

RHO_SLOPE = (RHO_MAX_DUTY-RHO_MIN_DUTY)/RHO_ANGLE_RANGE
RHO_OFFSET = (RHO_MAX_DUTY+RHO_MIN_DUTY)/2

# setup the GPIO pin for the servo
theta_servo_pin = 12
rho_servo_pin = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(theta_servo_pin,GPIO.OUT)
GPIO.setup(rho_servo_pin,GPIO.OUT)

# setup PWM process
theta_pwm = GPIO.PWM(theta_servo_pin,50) # 50 Hz (20 ms PWM period)
rho_pwm = GPIO.PWM(rho_servo_pin,50) # 50 Hz (20 ms PWM period)

theta_pwm.start(7)
rho_pwm.start(6.17)

#0.0042
k = 0.0050
k = 0

def SetThetaAngle(angle):
    #duty = 0.0556*angle + 7.2
    duty = -(slope)*angle + offset
    # print(duty)
    theta_pwm.ChangeDutyCycle(duty) # rotate to 0 degrees 0.6ms
    time.sleep(0.1)

def SetRhoAngle(angle):

    if angle < -20:
        angle = -20
    duty = RHO_SLOPE*angle + RHO_OFFSET
    print(duty)
    rho_pwm.ChangeDutyCycle(duty) # rotate to 0 degrees 0.6ms
    time.sleep(0.1)

def GetAtan(oposite, adyacent):
    radian_angle = math.atan(oposite/adyacent)
    degree_angle = radian_angle*180/math.pi
    return degree_angle

def GetThetaAngle(x,z):
    return GetAtan(x, z)

def GetRhoAngle(y,z):
    return GetAtan(y, z)

def Move(x,y,z):
    theta_angle = GetThetaAngle(x,z)
    rho_angle = GetRhoAngle(y,z)
    SetThetaAngle(theta_angle)
    SetRhoAngle(rho_angle)

#Move(0,0,360)

# SetThetaAngle(0)
SetRhoAngle(-10)


#pwm.ChangeDutyCycle(0) # this prevents jitter
#pwm.stop() # stops the pwm on 13
GPIO.cleanup() # good practice when finished using a pin