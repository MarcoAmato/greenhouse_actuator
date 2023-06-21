# Sirius Greenhouse Actuator

## Description
This is the code run on the Raspberry Pi actuator.
The host machine calls the main script with a command and eventual arguments.
Each command activates a different actuator.

## Commands
### water
Usage: `python3 -m actuator water <GPIO_pin> <seconds>`

Turns on the water pump connected to `GPIO_pin` for `seconds` seconds.
