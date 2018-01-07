"""
Created on 4 Jul 2016

http://tightdev.net/SpiDev_Doc.pdf
http://www.takaitra.com/posts/492

http://www.raspberrypi-spy.co.uk/2014/08/enabling-the-spi-interface-on-the-raspberry-pi/

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from spidev import SpiDev

from scs_host.lock.lock import Lock


# --------------------------------------------------------------------------------------------------------------------

class SPI(object):
    """
    classdocs
    """
    __LOCK_TIMEOUT =        1.0


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, bus, device, mode, max_speed):
        """
        Constructor
        """

        self.__bus = bus
        self.__device = device
        self.__mode = mode
        self.__max_speed = max_speed

        self.__connection = None


    # ----------------------------------------------------------------------------------------------------------------

    def open(self):
        if self.__connection:
            return

        Lock.acquire(SPI.__name__ + self.__bus, SPI.__LOCK_TIMEOUT)

        self.__connection = SpiDev()
        self.__connection.open(self.__bus, self.__device)

        self.__connection.mode = self.__mode
        self.__connection.max_speed_hz = self.__max_speed


    def close(self):
        if self.__connection is None:
            return

        self.__connection.close()
        self.__connection = None

        Lock.release(SPI.__name__ + self.__bus)


    # ----------------------------------------------------------------------------------------------------------------

    def xfer(self, args):
        self.__connection.xfer(args)


    def read_bytes(self, count):
        return self.__connection.readbytes(count)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SPI:{bus:%d, device:%s, mode:%d, max_speed:%d, connection:%s}" % \
               (self.__bus, self.__device, self.__mode, self.__max_speed, self.__connection)
