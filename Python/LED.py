"""
Provided to you by Emlid Ltd (c) 2014.
twitter.com/emlidtech || www.emlid.com || info@emlid.com

Example: Control the RGB LED onboard of Navio shield for Raspberry Pi

Please note that this example uses Adafruit I2C and PCA9685 drivers.

To run this example navigate to the directory containing it and run following commands:
sudo python3 LED.py
"""

# from Adafruit_PWM_Servo_Driver import PWM
from navio.adafruit_pwm_servo_driver import PWM
import time
import sys

import navio.gpio
import navio.util

navio.util.check_apm()

# drive Output Enable in PCA low
pin = navio.gpio.Pin(27)
pin.write(0)

pwm = PWM(0x40, debug=False)

# Set frequency to 60 Hz
pwm.setPWMFreq(60)

step = 1  # light color changing step

# set initial color
R = 0
G = 0
B = 4095
pwm.setPWM(0, 0, B)
print("LED is yellow")
time.sleep(1)

while True:
    for R in range(0, 4095, step):
        pwm.setPWM(2, 0, R)
    print("LED is green")
    time.sleep(1)

    for B in range(4095, 0, -step):
        pwm.setPWM(0, 0, B)
    print("LED is cyan")
    time.sleep(1)

    for G in range(0, 4095, step):
        pwm.setPWM(1, 0, G)
    print("LED is blue")
    time.sleep(1)

    for R in range(4095, 0, -step):
        pwm.setPWM(2, 0, R)
    print("LED is magenta")
    time.sleep(1)

    for B in range(0, 4095, step):
        pwm.setPWM(0, 0, B)
    print("LED is red")
    time.sleep(1)

    for G in range(4095, 0, -step):
        pwm.setPWM(1, 0, G)
    print("LED is yellow")
    time.sleep(1)

    # Change speed of continuous servo on channel 0
    # pwm.setPWM(0, 0, servoMin)
    # time.sleep(1)
    # pwm.setPWM(0, 0, servoMax)
    # time.sleep(1)
