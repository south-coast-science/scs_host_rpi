'''
Created on 4 Jul 2016

http://tightdev.net/SpiDev_Doc.pdf
http://www.takaitra.com/posts/492

http://www.raspberrypi-spy.co.uk/2014/08/enabling-the-spi-interface-on-the-raspberry-pi/

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
'''

import spidev


# --------------------------------------------------------------------------------------------------------------------

class HostSPI(object):
    '''
    classdocs
    '''
    __BUS = 0

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device, mode, max_speed):
        '''
        Constructor
        '''

        self.__device = device
        self.__mode = mode
        self.__max_speed = max_speed

        self.__bus = None


    # ----------------------------------------------------------------------------------------------------------------

    def open(self):
        if self.__bus:
            return

        self.__bus = spidev.SpiDev(HostSPI.__BUS, self.__device)

        self.__bus.mode = self.__mode
        self.__bus.max_speed_hz = self.__max_speed


    def close(self):
        self.__bus.close()
        self.__bus = None


    def xfer(self, args):
        self.__bus.xfer(args)


    def read_bytes(self, count):
        return self.__bus.readbytes(count)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "HostSPI:{device:%s, mode:%d, max_speed:%d}" % (self.__device, self.__mode, self.__max_speed)



