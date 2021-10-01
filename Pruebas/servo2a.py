import RPi.GPIO as GPIO
import time
import math

MIN_DUTY = 2.3
MAX_DUTY = 11

def SetAngle(pwm, angle):
    duty = 0.0556*angle + 7.2
    pwm.ChangeDutyCycle(duty) # rotate to 0 degrees 0.6ms
    time.sleep(1)



# setup the GPIO pin for the servo
servo_pin = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin,GPIO.OUT)

# setup PWM process
pwm = GPIO.PWM(servo_pin,50) # 50 Hz (20 ms PWM period)

pwm.start(7) # start PWM by rotating to 90 degrees

# SetAngle(pwm,-90)
#SetAngle(pwm,90)
# SetAngle(pwm,90)

#x_0 = 2.5
x_180 = 12.2

x_m = (x_180 + 2.5) / 2

#------------------#
#2.7ms 90 in x
#7.5ms 0 in x
#12.8ms -90 in x
#-------------------#

#2.4ms 0 in y
#7.3ms 90 in y
#12.2ms 180 in y

#2.75ms 0
#12.4ms 90

x_0 = 2.75
x_180 = 12.5
x_m = (x_0 + x_180) / 2

#y_0 = 2.4
y_180 = 12.1
y_m = (2.4 + y_180) / 2

slope = (x_180 - x_0) / 180
offset = x_m

def GetAngle(angle):
    if angle > 0:
        duty = -(slope) * angle + offset
    else:
        duty = -(slope + 0.004) * angle + offset
    return duty

# xx = 360
# zz = 360

# radian_angle = math.atan(xx/zz)
# degree_angle = radian_angle*180/math.pi


pwm.ChangeDutyCycle(GetAngle(30))
time.sleep(0.1)

time.sleep(0.3)

pwm.ChangeDutyCycle(GetAngle(60))
time.sleep(0.1)

time.sleep(0.3)

pwm.ChangeDutyCycle(GetAngle(-30))
time.sleep(0.1)


pwm.ChangeDutyCycle(0) # this prevents jitter
pwm.stop() # stops the pwm on 13
GPIO.cleanup() # good practice when finished using a pin