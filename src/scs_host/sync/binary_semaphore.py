"""
Created on 2 May 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A binary semaphore abstraction over the posix_ipc.Semaphore.

https://en.wikipedia.org/wiki/Semaphore_(programming)
http://semanchuk.com/philip/posix_ipc/#semaphore
"""

import posix_ipc


# --------------------------------------------------------------------------------------------------------------------

class BinarySemaphore(object):
    """
    classdocs
    """

    DEFAULT_ACQUISITION_TIME = 5.0                    # seconds

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, name, acquire_first):
        """
        Constructor
        """
        self.__name = name
        self.__semaphore = posix_ipc.Semaphore(self.name, flags=posix_ipc.O_CREAT)

        if not acquire_first:
            return

        try:
            self.__semaphore.acquire(self.DEFAULT_ACQUISITION_TIME)   # initial state: acquired by first creator
        except (posix_ipc.BusyError, posix_ipc.SignalError):
            pass


    # ----------------------------------------------------------------------------------------------------------------

    def acquire(self, timeout=None):                    # None timeout = wait forever (dangerous)
        try:
            self.__semaphore.acquire(timeout)

        except posix_ipc.BusyError:
            raise BusyError()

        except posix_ipc.SignalError:                   # on SIGTERM
            pass

        while self.__semaphore.value > 0:
            self.__semaphore.acquire(self.DEFAULT_ACQUISITION_TIME)     # limit the value to 0 or 1


    def release(self):
        self.__semaphore.release()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        return self.__name


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "BinarySemaphore:{name:%s}" % self.name


# --------------------------------------------------------------------------------------------------------------------

class BusyError(posix_ipc.BusyError):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        super(BusyError, self).__init__()
