# Sirius Greenhouse Actuator

## Description

This is the code run on the Raspberry Pi actuator.
The host machine calls the main script with a command and eventual arguments.
Each command activates a different actuator.

## Commands

The actuator listens for messages from the message broker from the .env configuration to water using a specific pin and for a specific amount of time.
