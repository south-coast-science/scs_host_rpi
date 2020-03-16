#!/usr/bin/env python3

"""
Created on 28 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_core.data.datetime import LocalizedDatetime
from scs_core.sampler.sampler import Sampler

from scs_host.sync.schedule_runner import ScheduleRunner


# --------------------------------------------------------------------------------------------------------------------

class TestSampler(Sampler):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, runner):
        """
        Constructor
        """
        Sampler.__init__(self, runner)


    # ----------------------------------------------------------------------------------------------------------------

    def sample(self):
        return 'SAMPLE: ' + LocalizedDatetime.now().utc().as_iso8601()


    def reset(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "TestSampler:{runner:%s}" % self.runner


# --------------------------------------------------------------------------------------------------------------------
# run...

schedule_runner = ScheduleRunner('scs-gases')
print(schedule_runner, file=sys.stderr)

sampler = TestSampler(schedule_runner)
print(sampler, file=sys.stderr)

sys.stderr.flush()

try:
    for sample in sampler.samples():
        print(sample, file=sys.stderr)
        sys.stderr.flush()

except KeyboardInterrupt:
    pass
