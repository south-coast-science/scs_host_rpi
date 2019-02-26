"""
Created on 12 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_host.sys.host_gpio import HostGPIO


# --------------------------------------------------------------------------------------------------------------------

# noinspection PyUnusedLocal,PyAbstractClass
class HostGPI(HostGPIO):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, pin):
        raise NotImplementedError()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def state(self):
        raise NotImplementedError()


    def wait(self, edge):
        raise NotImplementedError()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        raise NotImplementedError()

