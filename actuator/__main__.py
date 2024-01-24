import configparser
import sys
import stomp # for message broker
import socket # for hostname retrieval
import re # to split the hostname in letters and numbers
import os

from actuator.pump_script import pump_water
from actuator.queue.subscriber import Subscriber

usage = """
Usage:
python -m actuator <command> <parameters>
"""
def load_env_file(env_file_path=".env"):
    try:
        with open(env_file_path, "r") as file:
            for line in file:
                # Ignore lines that are empty or start with '#'
                if not line.strip() or line.startswith("#"):
                    continue

                # Split the line at the first '=' character
                key, value = line.strip().split("=", 1)

                # Set the environment variable
                os.environ[key] = value

    except FileNotFoundError:
        print(f"{env_file_path} not found. Make sure to create a .env file with your environment variables.")


def main():
    load_env_file()
    url = os.getenv("URL")
    username = os.getenv("USER")
    password = os.getenv("PASS")

    # Get hostname for the queue
    hostname = socket.gethostname()
    r = re.compile("([a-zA-Z]+)([0-9]+)")
    m = r.match(hostname)
    # Match the tuple <T.i.A>
    queue_destination = m.group(1) + "." + m.group(2) + ".water"

    conn = stomp.Connection(host_and_ports=[(url, 61613)])
    conn.set_listener('', Subscriber(conn))
    conn.connect(username, password, wait=True)
    conn.subscribe(destination=queue_destination, id=1, ack='auto')

    while 1:
        time.sleep(10)


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
