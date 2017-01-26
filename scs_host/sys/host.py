"""
Created on 16 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import os
import subprocess

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


    @staticmethod
    def enable_eeprom_write():
        # WARNING: may require restart for sensor I2C bus to function again
        subprocess.call(['sudo', 'dtoverlay', 'i2c-gpio', 'i2c_gpio_sda=0', 'i2c_gpio_scl=1'])

