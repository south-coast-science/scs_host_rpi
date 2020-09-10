#!/usr/bin/env python3

"""
Created on 10 Sep 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_host.sys.nmcli import NMCLi

# --------------------------------------------------------------------------------------------------------------------

# sudo killall -STOP NetworkManager

report = NMCLi.find()
print(report)
