import RPi.GPIO as GPIO
import time

MIN_DUTY = 2.3
MAX_DUTY = 11

def SetAngle(pwm, angle):
    duty = 0.0556*angle + 7.2
    pwm.ChangeDutyCycle(duty) # rotate to 0 degrees 0.6ms
    time.sleep(1)



# setup the GPIO pin for the servo
servo_pin = 13
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
#2.5ms 0 in x
#7.4ms 90 in x
#12.2ms 180 in x
#-------------------#

#2.4ms 0 in y
#7.3ms 90 in y
#12.2ms 180 in y


for ii in range(0,1):
     pwm.ChangeDutyCycle(12.2)#rotate to 0 degrees 0.6ms
     time.sleep(1)
     #pwm.ChangeDutyCycle(7.0) # rotate to 90 degrees 1.4ms
     #time.sleep(1)
     #pwm.ChangeDutyCycle(12) # rotate to 180 degrees 2.4ms
     #time.sleep(1)


pwm.ChangeDutyCycle(0) # this prevents jitter
pwm.stop() # stops the pwm on 13
GPIO.cleanup() # good practice when finished using a pin