import time, threading
# import RPi.GPIO as GPIO 
from enum import Enum

class State(Enum):
   GREEN = 1
   RED = 0

interrupt_time_in_s = 0.2


GREEN_TIME_IN_S = 3
RED_TIME_IN_S = 9


state = State.RED
time_in_state = 0

# GPIO.setmode(GPIO.BCM) 

# SHOOT_GPIO = 18
# REDGREEN_GPIO = 16

# GPIO.setup(SHOOT_GPIO, GPIO.OUT, initial = 0)
# GPIO.setup(REDGREEN_GPIO, GPIO.OUT, initial = 0)

def Shoot():
    #Set GPIO 1
    # GPIO.output(SHOOT_GPIO, 1)
    time.sleep(0.01)
    # GPIO.output(SHOOT_GPIO, 0)
    #Set GPIO 0
   
def HandleGreenRedTimes():
    global time_in_state
    global state

    time_in_state += interrupt_time_in_s

    if state == State.RED:
        print(f"Red [{time_in_state:.2f} s]")
        # Set GPIO to 0
        # GPIO.output(REDGREEN_GPIO, 0)
        if time_in_state >= RED_TIME_IN_S:
            state = State.GREEN
            time_in_state = 0
    else:
        print(f"Green [{time_in_state:.2f} s]")
        # Set GPIO to 1
        # GPIO.output(REDGREEN_GPIO, 1)
        if time_in_state >= GREEN_TIME_IN_S:
            state = State.RED
            time_in_state = 0

def OneSecondPassed():
    
    Shoot()
    HandleGreenRedTimes()
    
    threading.Timer(interrupt_time_in_s, OneSecondPassed).start()

time.sleep(interrupt_time_in_s)

OneSecondPassed()


