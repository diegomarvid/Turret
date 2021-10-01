from time import sleep
from piservo import Servo


servo = Servo(12, min_value=0, max_value=180, min_pulse=0.55, max_pulse=2.5, frequency=50)

angle = -45

servo.write(90 - angle)
sleep(0.2)

# for i in range(0,180,2):
#     servo.write(i)
#     sleep(0.2)


# print(servo.read())


