#!/usr/bin/env python3

"""
Created on 28 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_core.data.localized_datetime import LocalizedDatetime

from scs_host.sync.schedule_runner import ScheduleRunner


# --------------------------------------------------------------------------------------------------------------------

class TestRunner(ScheduleRunner):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, name):
        """
        Constructor
        """
        ScheduleRunner.__init__(self, name, True)


    # ----------------------------------------------------------------------------------------------------------------

    def sample(self):
        return 'SAMPLE ' + LocalizedDatetime.now().as_iso8601()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "TestRunner:{name:%s}" % self.name


# --------------------------------------------------------------------------------------------------------------------
# run...

runner = TestRunner('scs-gases')
print(runner, file=sys.stderr)
sys.stderr.flush()

try:
    for sample in runner.samples():
        print(sample, file=sys.stderr)
        sys.stderr.flush()

except KeyboardInterrupt:
    pass
