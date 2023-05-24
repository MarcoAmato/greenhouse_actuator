import configparser
import sys

from actuator.pump_script import pump_water

usage = """
Usage:
python -m actuator <command> <parameters>
"""


def main():
    config = initialize_config()
    # get first main parameter
    command = sys.argv[1]
    # based on the first parameter of main, execute the corresponding actuator script
    if command == "pump":
        water_pump_actuator(config)
    else:
        print("Invalid command")
        print(usage)


def initialize_config():
    # get config file
    config = configparser.ConfigParser()
    # check if config file exists
    if not config.read("config.ini"):
        print("Config file not found. Please create a config.ini file in the root directory following the structure "
              "of config.ini.example.")
        sys.exit(1)
    return config


def water_pump_actuator(config):
    # second parameter of main is the time in seconds
    sec = int(sys.argv[2])
    # get GPIO pin from config.ini file
    output_pin = int(config["GPIO_PINS"]["pump_pin"])
    # execute the pump script for the given time
    pump_water(sec, output_pin)


if __name__ == "__main__":
    """
    This main is executed from the host machine. It executes the corresponding actuator script based on the first
    parameter of main.
    
    Usage:
    python3 -m actuator <command> <parameters>
    """
    main()
