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
    match command:
        case "pump":
            # second parameter is the time in seconds
            sec = int(sys.argv[2])
            # execute the pump script for the given time
            pump_water(sec)

        case _:  # default case
            print("Invalid command")
            print(usage)


if "__name__" == "__main__":
    """
    This main is executed from the host machine. It executes the corresponding actuator script based on the first
    parameter of main.
    
    Usage:
    python -m actuator <command> <parameters>
    """
    main()
