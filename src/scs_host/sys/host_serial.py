"""
Created on 19 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Warning: for Raspberry Pi systems, dev/ttyAMA0 (a.k.a. /dev/ttyS0) must not be a serial console, and must be enabled.
"""

import serial

from scs_core.sys.serial import Serial

from scs_host.lock.lock import Lock


# --------------------------------------------------------------------------------------------------------------------

class HostSerial(Serial):
    """
    classdocs
    """

    __PORT_PREFIX =     "/dev/serial"                 # hard-coded path

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, port_number, baud_rate, hard_handshake=False):
        """
        Constructor
        """
        super().__init__(port_number, baud_rate, hard_handshake)

        if hard_handshake:
            raise NotImplementedError("hard_handshake")


    # ----------------------------------------------------------------------------------------------------------------

    def open(self, lock_timeout, comms_timeout):
        # lock...
        Lock.acquire(self.__lock_name, lock_timeout)

        # serial...
        self._ser = serial.Serial(port=self.device_identifier, baudrate=self._baud_rate, timeout=comms_timeout)


    def close(self):
        try:
            # port...
            if self._ser:
                self._ser.close()
                self._ser = None

        finally:
            # lock...
            Lock.release(self.__lock_name)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def device_identifier(self):
        return self.__PORT_PREFIX + str(self._device_identifier)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def __lock_name(self):
        return "%s-%s" % (self.__class__.__name__, self._device_identifier)
