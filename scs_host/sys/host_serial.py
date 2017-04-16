"""
Created on 10 Jan 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""


# TODO: implement HostSerial
# TODO: add lock functionality

# --------------------------------------------------------------------------------------------------------------------

class HostSerial(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, port_number, baud_rate, hard_handshake=False):
        """
        Constructor
        """
        self.__port_number = port_number
        self.__baud_rate = baud_rate
        self.__hard_handshake = hard_handshake

        self.__ser = None


    # ----------------------------------------------------------------------------------------------------------------

    def open(self, timeout):
        pass


    def close(self):
        if self.__ser is None:
            return

        pass


    # ----------------------------------------------------------------------------------------------------------------

    # noinspection PyUnusedLocal
    def read_line(self, terminator, timeout):
        return ''


    # noinspection PyUnusedLocal
    def write_line(self, text):
        return 0


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "HostSerial:{port_number:%d, baud_rate=%d, hard_handshake=%s, serial:%s}" % \
                    (self.__port_number, self.__baud_rate, self.__hard_handshake, self.__ser)
