import RPi.GPIO as GPIO
from time import sleep


def pump_water(sec, pump_pin):
    print("Pumping water for {} seconds...".format(sec))

    # set GPIO mode and set up the pump pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pump_pin, GPIO.OUT)

    try:
        sleep(0.5)

        # turn the pump on for the given time
        for x in range(0, sec):
            GPIO.output(pump_pin, GPIO.HIGH)
            sleep(1)
            GPIO.output(pump_pin, GPIO.LOW)
            sleep(1)

        # turn the pump off
        GPIO.cleanup()

        print("Done pumping water.")

    except KeyboardInterrupt:
        # stop pump when ctrl-c is pressed
        GPIO.cleanup()
