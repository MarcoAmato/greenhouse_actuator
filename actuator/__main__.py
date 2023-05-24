import configparser
import sys

from actuator.pump_script import pump_water

usage = """
Usage:
python3 -m actuator <command> <parameters>
"""


def main():
    check_python_version()
    # get config file
    config = configparser.ConfigParser()
    # get first main parameter
    command = sys.argv[1]
    # based on the first parameter of main, execute the corresponding actuator script
    match command:
        case "pump":
            water_pump_actuator(config)

        case _:  # default case
            print("Invalid command")
            print(usage)


if "__name__" == "__main__":
    """
    This main is executed from the host machine. It executes the corresponding actuator script based on the first
    parameter of main.
    
    Usage:
    python3 -m actuator <command> <parameters>
    """
    main()


def water_pump_actuator(config):
    # second parameter of main is the time in seconds
    sec = int(sys.argv[2])
    # get GPIO pin from config.ini file
    output_pin = config["GPIO_PINS"]["pump_pin"]
    # execute the pump script for the given time
    pump_water(sec, output_pin)


def check_python_version():
    if sys.version_info[0:2] != (3, 10):
        # print command to install python 3.10
        raise Exception('Requires python 3.10. Found: ' + sys.version + '.\n' + "Run 'sudo apt install python3.10'")
