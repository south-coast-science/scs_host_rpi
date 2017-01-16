"""
Created on 16 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import os

from scs_host.sys.mcu_datum import MCUDatum


# --------------------------------------------------------------------------------------------------------------------

class Host(object):
    """
    Broadcom BCM2837 64bit ARMv7 quad core processor
    """

    I2C_EEPROM =        3
    I2C_SENSORS =       1

    SCS_CONF = '/home/pi/SCS/conf/'
    SCS_OSIO = '/home/pi/SCS/osio/'


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def mcu_temp():
        message = str(os.popen("vcgencmd measure_temp").readline())

        message = message.replace("temp=", "").replace("'C\n", "")

        temp = float(message)

        return MCUDatum(temp)
