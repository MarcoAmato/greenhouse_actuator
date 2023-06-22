import configparser
import sys

from actuator.pump_script import pump_water

usage = """
Usage:
python -m actuator <command> <parameters>
"""


def main():
    # get first main parameter
    command = sys.argv[1]
    # based on the first parameter of main, execute the corresponding actuator script
    if command == "water":
        water_pump_actuator()
    else:
        print("Invalid command")
        print(usage)


def water_pump_actuator():
    # second parameter of main is the GPIO pin of the water pump
    water_pump_pin = int(sys.argv[2])

    # third parameter of main is the time in seconds
    sec = int(sys.argv[3])

    # execute the pump script for the given time
    pump_water(sec, water_pump_pin)


if __name__ == "__main__":
    """
    This main is executed from the host machine. It executes the corresponding actuator script based on the first
    parameter of main.
    
    Usage:
    python3 -m actuator <command> <parameters>
    """
    main()
