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

    DFE_EEPROM_ADDR =   0x50

    DFE_EEP_IMAGE =     "/home/pi/SCS/hat.eep"              # hard-coded path

    SCS_LOCK =          "/run/lock/southcoastscience/"      # hard-coded path

    SCS_TMP =           "/tmp/southcoastscience/"           # hard-coded path

    __SCS_CONF =        "/home/pi/SCS/conf/"                # hard-coded path
    __SCS_OSIO =        "/home/pi/SCS/osio/"                # hard-coded path


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def power_cycle():
        subprocess.call(['sudo', 'reboot'])


    @staticmethod
    def enable_eeprom_access():
        subprocess.call(['sudo', 'dtoverlay', 'i2c-gpio', 'i2c_gpio_sda=0', 'i2c_gpio_scl=1'])


    @staticmethod
    def mcu_temp():
        message = str(os.popen("vcgencmd measure_temp").readline())

        message = message.replace("temp=", "").replace("'C\n", "")

        temp = float(message)

        return MCUDatum(temp)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def conf_dir(cls):
        return cls.__SCS_CONF


    @classmethod
    def osio_dir(cls):
        return cls.__SCS_OSIO
