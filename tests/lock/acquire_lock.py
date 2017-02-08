#!/usr/bin/env python3

"""
Created on 8 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import os
import time

from scs_host.lock.lock import Lock


# --------------------------------------------------------------------------------------------------------------------

print("pid:%d" % os.getpid())


# --------------------------------------------------------------------------------------------------------------------

name = "TestLock"

exists = Lock.exists(name)
print("exists: %s" % exists)

pid = Lock.pid(name)
print("pid: %s" % str(pid))

print("-")


# --------------------------------------------------------------------------------------------------------------------

Lock.acquire(name, 4.0)

print("locked...")

try:
    exists = Lock.exists(name)
    print("exists: %s" % exists)

    pid = Lock.pid(name)
    print("pid: %s" % str(pid))

    print("-")

    while True:
        time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    Lock.release(name)

    print()
    print("unlocked")
