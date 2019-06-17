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
    wifi (brcmfmac), B8:27:EB:56:50:8F, hw, mtu 1500
    inet4 192.168.1.122/24
    inet6 fe80::212a:9d31:4b3e:59c/64
"""

import re
import subprocess

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class NMCLi(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def find(cls):
        try:
            p = subprocess.Popen(['nmcli'], stdout=subprocess.PIPE)
            report = p.communicate()
            lines = report[0].decode().split('\n')

        except FileNotFoundError:
            return None

        connections = cls.parse(lines)

        return NMCLi(connections)


    @classmethod
    def parse(cls, lines):
        connections = OrderedDict()

        for line in lines:
            match = re.match(r'([a-z]+[0-9]+): connected to (.+)$', line.strip())

            if match is None:
                continue

            fields = match.groups()
            port = fields[0]
            network = fields[1]

            connections[port] = network

        return connections


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, connections):
        """
        Constructor
        """
        self.__connections = connections


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
