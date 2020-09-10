"""
Created on 17 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

eth0: connected to Wired connection 1
    "TP-LINK USB 10/100/1000 LAN"
    ethernet (r8152), 98:DE:D0:04:9B:CC, hw, mtu 1500
    ip4 default
    inet4 192.168.1.88/24
    inet6 fe80::131d:325a:f7bd:e3e/64

wlan0: connected to TP-Link_0F04
    "Broadcom "
    wifi (device), B8:27:EB:56:50:8F, hw, mtu 1500
    inet4 192.168.1.122/24
    inet6 fe80::212a:9d31:4b3e:59c/64
"""

import re
import sys
import time

from collections import OrderedDict
from subprocess import Popen, TimeoutExpired, PIPE

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class NMCLi(JSONable):
    """
    classdocs
    """

    TIMEOUT = 60.0                              # seconds
    RESTART_WAIT = 20.0                         # seconds

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def find(cls):
        lines = cls.__nmcli()
        connections = cls.parse(lines)

        return cls(connections)


    @classmethod
    def parse(cls, lines):
        connections = OrderedDict()

        if not lines:
            return connections

        for line in lines:
            match = re.match(r'([^: ]+): connected to (.+)$', line.strip())

            if match is None:
                continue

            fields = match.groups()
            port = fields[0]
            network = fields[1]

            connections[port] = network

        return connections


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __nmcli(cls):
        while True:
            try:
                p = Popen(['nmcli'], stdout=PIPE)
                report = p.communicate(timeout=cls.TIMEOUT)

                return report[0].decode().split('\n')

            except FileNotFoundError:
                return None

            except TimeoutExpired:
                print("NMCLi: restarting NetworkManager", file=sys.stderr)
                sys.stderr.flush()

                Popen(['sudo', 'systemctl', 'restart', 'NetworkManager'])
                time.sleep(cls.RESTART_WAIT)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, connections):
        """
        Constructor
        """
        self.__connections = connections                    # dictionary


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['conns'] = self.connections

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def connections(self):
        return self.__connections


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NMCLi:{connections:%s}" % self.connections
