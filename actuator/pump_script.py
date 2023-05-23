import RPi.GPIO as GPIO
from time import sleep
import sys


def pump_water(sec):
    GPIO.setmode(GPIO.BCM)
    # TODO make config.ini file for GPIO pins. For now, use 18
    gpio = int(sys.argv[2]) or 18

    GPIO.setup(gpio, GPIO.OUT)

    try:
        # turn the pump off and on for 0.25 seconds to prime the pump
        GPIO.output(gpio, GPIO.LOW)
        sleep(0.25)

        # turn the pump on for the given time
        GPIO.output(gpio, GPIO.HIGH)
        sleep(sec)

        # turn the pump off
        GPIO.cleanup()

    except KeyboardInterrupt:
        # stop pump when ctrl-c is pressed
        GPIO.cleanup()
