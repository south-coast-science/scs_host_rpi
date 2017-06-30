#!/usr/bin/env python3

"""
Created on 28 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_core.data.localized_datetime import LocalizedDatetime

from scs_host.sync.semaphore_sampler import SemaphoreSampler


# --------------------------------------------------------------------------------------------------------------------

class TestSampler(SemaphoreSampler):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, name):
        """
        Constructor
        """
        SemaphoreSampler.__init__(self, name, True)


    # ----------------------------------------------------------------------------------------------------------------

    def sample(self):
        return 'SAMPLE ' + LocalizedDatetime.now().as_iso8601()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "TestSampler:{name:%s}" % self.name


# --------------------------------------------------------------------------------------------------------------------
# run...

sampler = TestSampler('scs-gases')
print(sampler, file=sys.stderr)
sys.stderr.flush()

try:
    for sample in sampler.samples():
        print(sample, file=sys.stderr)
        sys.stderr.flush()

except KeyboardInterrupt:
    pass