import sys
import stomp # for message broker
import socket # for hostname retrieval
import re # to split the hostname in letters and numbers
import os
import json
import time

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


def load_config_json():
    # read the config.json file if it exists
    try:
        with open("./config.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("config.json not found. Using default.")
        return None


def main():
    load_env_file()
    url = os.getenv("URL")
    username = os.getenv("USER")
    password = os.getenv("PASS")

    configuration = load_config_json()
    try:
        # Create a single connection for all queues
        conn = stomp.Connection(host_and_ports=[(url, 61613)])
        conn.set_listener('', Subscriber(conn))
        conn.connect(username, password, wait=True)

        if configuration is not None:
            # If configuration file exists, subscribe to multiple queues
            ids = configuration["actuator_id"]
            for id in ids:
                queue_destination = f"actuator.{str(id)}.water"
                try:
                    conn.subscribe(destination=queue_destination, id=id, ack='auto')
                    print(f"Subscribed to queue: {queue_destination}")
                except Exception as e:
                    print(f"Failed to subscribe to queue {queue_destination}: {str(e)}")
        else:
            # Fallback to hostname-based queue
            hostname = socket.gethostname()
            r = re.compile("([a-zA-Z]+)([0-9]+)")
            m = r.match(hostname)
            if m:
                queue_destination = f"{m.group(1)}.{m.group(2)}.water"
                conn.subscribe(destination=queue_destination, id=1, ack='auto')
                print(f"Subscribed to queue: {queue_destination}")
            else:
                raise ValueError("Invalid hostname format")

        # Keep the connection alive
        while True:
            time.sleep(10)

    except stomp.exception.ConnectFailedException:
        print("Failed to connect to ActiveMQ broker")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.disconnect()


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
