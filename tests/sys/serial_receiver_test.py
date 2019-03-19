#!/usr/bin/env python3

"""
Created on 19 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://www.raspberrypi.org/documentation/configuration/uart.md
"""

# from scs_host.sys.host import Host
from scs_host.sys.host_serial import HostSerial



# --------------------------------------------------------------------------------------------------------------------

"""
import serial


ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
)

try:
    # ser.open()

    while True:
        line = ser.readline().decode().strip()
        print(line)

finally:
    ser.close()
"""

serial = None

try:
    serial = HostSerial(0, 9600, False)
    serial.open(4, 2)
    print(serial)

    while True:
        line = serial.read_line(HostSerial.EOL, 10)
        print(line)

except KeyboardInterrupt:
    print()

finally:
    if serial:
        serial.close()

