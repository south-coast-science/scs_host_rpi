#!/usr/bin/env python3

'''
Created on 4 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
'''

from scs_host.sys.hostname import Hostname

from scs_core.common.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

hostname = Hostname.find()
print(hostname)
print("-")

print(JSONify.dumps(hostname))
print("=")

