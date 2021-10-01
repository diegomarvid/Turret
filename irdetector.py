#!/usr/bin/env python

from time import sleep           # Allows us to call the sleep function to slow down our loop
import RPi.GPIO as GPIO           # Allows us to call our GPIO pins and names it just GPIO
import csv

GPIO.setmode(GPIO.BCM)           # Set's GPIO pins to BCM GPIO numbering
INPUT_PIN = 4           # Sets our input pin, in this example I'm connecting our button to pin 4. Pin 0 is the SDA pin so I avoid using it for sensors/buttons
GPIO.setup(INPUT_PIN, GPIO.IN)           # Set our input pin to be an input
VIDAS = 20

while True: 
        #    if (GPIO.input(INPUT_PIN) == True): # Physically read the pin now
                    # print('1')
           if (GPIO.input(INPUT_PIN) == False):
                VIDAS = VIDAS - 1
                print(f"manchado | Health: {VIDAS} ")
                sleep(25/1000); 
           sleep(0.5/1000);           # Sleep for a full second before restarting our loop

# header = ['data']

# with open('resources/ir.csv', 'w') as f:

#     writer = csv.writer(f)

#     writer.writerow(header)

#     while True: 
#         if (GPIO.input(INPUT_PIN) == True): # Physically read the pin now
#                 writer.writerow('1')
#         if (GPIO.input(INPUT_PIN) == False):
#                 writer.writerow('0')
#         sleep(1/1000)


