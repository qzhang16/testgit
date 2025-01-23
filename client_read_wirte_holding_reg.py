#!/usr/bin/env python3

"""
Modbus Client for reading and writing to holding registers.

This script connects to a Modbus server, writes random values to the first 5 holding
registers, increments each of these values and writes them to the next 5 holding registers,
toggles boolean flag values every 300 seconds, and regularly reads and prints the register values.
"""

import time
import random
from pyModbusTCP.client import ModbusClient

# Modbus server IP and port (update with your server's IP and port)
MODBUS_SERVER_IP = '192.168.1.201'  # Replace with your server's IP address
MODBUS_SERVER_PORT = 5020  # Default Modbus port (can be changed if needed)

# Initialize Modbus client
#c = ModbusClient(host=MODBUS_SERVER_IP, port=MODBUS_SERVER_PORT,unit_id=1, auto_open=True)
c = ModbusClient(host="192.168.1.201", port=5020, unit_id=1, auto_open=True)
print("connected")
# Flag values to toggle on and off
boolen_flag_values_off = [0, 0, 0, 0, 0]
boolen_flag_values_on = [1, 1, 1, 1, 1]

# Default values for registers
default_values = [0, 0, 0, 0, 0]

# Record the start time for timing the 30-second interval
start_time = time.time()

# Flag to control toggling of boolean values
flag_val = False

# Main loop to continually read/write Modbus registers
while True:
    # Get the current time
    current_time = time.time()

    # Generate random values for 5 registers (between 1 and 500)
    random_values = [random.randint(1, 500) for _ in range(5)]

    # Increment each value in default_values by 1
    default_values = [val + 1 for val in default_values]
    for item in default_values:
        random_values.append(item)

    # Every 30 seconds, toggle the boolean flag values
    if current_time - start_time >= 3600:
        # Reset the start time for the next interval
        start_time = current_time

        # Toggle the boolean flag values (on/off)
        if flag_val:
            for item in boolen_flag_values_off:
                random_values.append(item)
            flag_val = False
        else:
            for item in boolen_flag_values_on:
                random_values.append(item)
            flag_val = True

    # Write the generated random values to the holding registers (address 0)
    # TCP auto connect on first modbus request
    #c = ModbusClient(host="localhost", port=502, unit_id=1, auto_open=True)
    if c.write_multiple_registers(0, random_values):
        print(f"Written random values to registers: {random_values}")
    else:
        print("Failed to write to registers")

    # Read the 15 holding registers starting from address 0
    regs_l = c.read_holding_registers(0, 15)

    # If successful, print the values of the registers
    if regs_l:
        print('Register values from address #0 to #9: %s' % regs_l)
        print('\r\n')
    else:
        print('Unable to read registers')

    # Sleep for 5 seconds before the next loop iteration
    time.sleep(5)
