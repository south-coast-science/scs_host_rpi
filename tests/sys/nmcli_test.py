#!/usr/bin/env python3

"""
Created on 17 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify

from scs_host.sys.nmcli import NMCLi


# --------------------------------------------------------------------------------------------------------------------

response = [
    'eth0: connected to Wired connection 1',
    '	"TP-LINK USB 10/100/1000 LAN"',
    '    ethernet (r8152), 98:DE:D0:04:9B:CC, hw, mtu 1500',
    '    ip4 default',
    '    inet4 192.168.1.88/24',
    '    inet6 fe80::131d:325a:f7bd:e3e/64',
    '',
    'wlan0: connected to TP-Link_0F04',
    '    "Broadcom "',
    '    wifi (brcmfmac), B8:27:EB:56:50:8F, hw, mtu 1500',
    '    inet4 192.168.1.122/24',
    '    inet6 fe80::212a:9d31:4b3e:59c/64',
    '',
    'lo: unmanaged',
    '    loopback (unknown), 00:00:00:00:00:00, sw, mtu 65536']

conns = NMCLi.parse(response)
print(conns)
print("-")

nmcli = NMCLi(conns)
print(nmcli)
print("-")

print(JSONify.dumps(nmcli))
print("-")

print("find...")
nmcli = NMCLi.find()
print(nmcli)
