"""
Created on 26 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A Unix domain socket abstraction, implementing ProcessComms

Only one reader per UDS!

https://pymotw.com/2/socket/uds.html
"""

import os
import socket
import sys
import time

from scs_core.sys.process_comms import ProcessComms


# --------------------------------------------------------------------------------------------------------------------

class DomainSocket(ProcessComms):
    """
    classdocs
    """

    __BACKLOG = 1          # number of unaccepted connections the system will allow before refusing new connections
    __BUFFER_SIZE = 1024

    __WAIT_FOR_AVAILABILITY = 10.0      # seconds

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __read(cls, connection):
        message = b''

        while True:
            data = connection.recv(cls.__BUFFER_SIZE)

            if not data:
                break

            message += data

        return message.decode()


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, address):
        """
        Constructor
        """
        self.__address = address            # string
        self.__socket = None                # socket.socket


    # ----------------------------------------------------------------------------------------------------------------

    def connect(self, wait_for_availability=True):
        self.__socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        # while True:
        #     try:
        #         self.__socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        #
        #     except ConnectionRefusedError as ex:
        #         if not wait_for_availability:
        #             raise ex
        #
        #         print("*** DomainSocket.connect: waiting for availability.", file=sys.stderr)
        #         sys.stderr.flush()
        #
        #         time.sleep(self.__WAIT_FOR_AVAILABILITY)


    def close(self):
        if self.__socket:
            self.__socket.close()


    # ----------------------------------------------------------------------------------------------------------------

    def read(self):                                             # blocking
        # socket...
        self.__socket.bind(self.__address)
        self.__socket.listen(DomainSocket.__BACKLOG)

        try:
            while True:
                connection, _ = self.__socket.accept()

                try:
                    # data...
                    yield DomainSocket.__read(connection).strip()

                finally:
                    connection.close()

        finally:
            os.unlink(self.__address)


    def write(self, message, wait_for_availability=True):       # message is dispatched on close()
        # socket...
        while True:
            try:
                self.__socket.connect(self.__address)
                break

            except (socket.error, FileNotFoundError) as ex:
                print("DomainSocket.write: %s" % ex, file=sys.stderr)
                sys.stderr.flush()

                if not wait_for_availability:
                    raise ex

                time.sleep(self.__WAIT_FOR_AVAILABILITY)

        # data...
        self.__socket.sendall(message.strip().encode())


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def address(self):
        return self.__address


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DomainSocket:{address:%s, socket:%s}" % (self.address, self.__socket)
