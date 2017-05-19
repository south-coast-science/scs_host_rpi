"""
Created on 12 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""


# --------------------------------------------------------------------------------------------------------------------

class HostGPIO(object):
    """
    classdocs
    """
    IN =        None
    OUT =       None

    RISING =    None
    FALLING =   None

    HIGH =      None
    LOW =       None


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def cleanup():
        raise NotImplementedError


    @staticmethod
    def setup(pin, direction):
        raise NotImplementedError


    @staticmethod
    def input(pin):
        raise NotImplementedError


    @staticmethod
    def output(pin, direction):
        raise NotImplementedError


    @staticmethod
    def wait_for_edge(pin, edge):
        raise NotImplementedError
