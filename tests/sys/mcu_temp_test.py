#!/usr/bin/env python3

"""
Created on 20 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

while True:
    temp = Host.mcu_temp()
    print(temp)
    print("-")

    time.sleep(1)
