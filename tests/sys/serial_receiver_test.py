#!/usr/bin/env python3

"""
Created on 19 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://www.raspberrypi.org/documentation/configuration/uart.md
"""

from scs_host.sys.host_serial import HostSerial


# --------------------------------------------------------------------------------------------------------------------

serial = None

try:
    serial = HostSerial(0, 9600, False)
    serial.open(4, 2)
    print(serial)

    for line in serial.read_lines(timeout=10):
        print(line)

except KeyboardInterrupt:
    print()

finally:
    if serial:
        serial.close()

