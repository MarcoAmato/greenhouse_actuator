# Sirius Greenhouse Actuator

## Description
This is the code run on the Raspberry Pi actuator.
The host machine calls the main script with a command and eventual arguments.
Each command activates a different actuator.

## Commands
### Pump
Usage: `python3 -m actuator pump <seconds>`

Turns on the pump for the specified number of seconds.
