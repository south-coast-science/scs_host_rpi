"""
Created on 16 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://raspberrypi.stackexchange.com/questions/2086/how-do-i-get-the-serial-number
"""

import os
import re
import socket
import subprocess

from pathlib import Path

from scs_core.sys.disk_usage import DiskUsage
from scs_core.sys.ipv4_address import IPv4Address
from scs_core.sys.node import Node

from scs_host.sys.mcu_datum import MCUDatum


# TODO: fix EEPROM access

# --------------------------------------------------------------------------------------------------------------------

class Host(Node):
    """
    Broadcom BCM2837 64bit ARMv7 quad core processor
    """

    OS_ENV_PATH =           'SCS_ROOT_PATH'

    I2C_EEPROM =            3
    I2C_SENSORS =           1

    DFE_EEPROM_ADDR =       0x50
    DFE_UID_ADDR =          0x58


    # ----------------------------------------------------------------------------------------------------------------
    # devices...

    __OPC_SPI_BUS =         0                                   # based on spidev
    __OPC_SPI_DEVICE =      0                                   # based on spidev

    __NDIR_SPI_BUS =        0                                   # based on spidev
    __NDIR_SPI_DEVICE =     1                                   # based on spidev

    __NDIR_USB_DEVICE =     "/dev/ttyUSB0"                      # hard-coded path
    __GPS_SERIAL_DEVICE =   0                                   # hard-coded path (should be 0 on full-fat pies)


    # ----------------------------------------------------------------------------------------------------------------
    # time marker...

    __TIME_SYNCHRONIZED =  "/run/systemd/timesync/synchronized"


    # ----------------------------------------------------------------------------------------------------------------
    # directories and files...

    __DEFAULT_HOME_DIR =    "/home/pi"                          # hard-coded abs path
    __LOCK_DIR =            "/run/lock/southcoastscience"       # hard-coded abs path
    __TMP_DIR =             "/tmp/southcoastscience"            # hard-coded abs path

    __SCS_DIR =             "SCS"                               # hard-coded rel path

    __COMMAND_DIR =         "cmd"                               # hard-coded rel path
    __CONF_DIR =            "conf"                              # hard-coded rel path
    __AWS_DIR =             "aws"                               # hard-coded rel path
    __OSIO_DIR =            "osio"                              # hard-coded rel path

    __LATEST_UPDATE =       "latest_update.txt"                 # hard-coded rel path
    __DFE_EEP_IMAGE =       "dfe_cape.eep"                      # hard-coded rel path


    # ----------------------------------------------------------------------------------------------------------------
    # host acting as DHCP server...

    __SERVER_ADDRESS =      '172.22.15.1'                       # had-coded abs path


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def serial_number():
        cpuinfo = os.popen("cat /proc/cpuinfo").readlines()
        line = cpuinfo[-1]

        match = re.match(r'Serial\s*:\s*([0-9A-Fa-f]+)', line)

        if match is None:
            return None

        fields = match.groups()
        serial = fields[0]

        return serial


    @staticmethod
    def enable_eeprom_access():
        subprocess.call(['sudo', 'dtoverlay', 'i2c-gpio', 'i2c_gpio_sda=0', 'i2c_gpio_scl=1'])


    @staticmethod
    def mcu_temp():
        message = str(os.popen("vcgencmd measure_temp").readline())

        message = message.replace("temp=", "").replace("'C\n", "")

        temp = float(message)

        return MCUDatum(temp)


    @classmethod
    def shutdown(cls):
        subprocess.call(['sudo', 'shutdown', 'now'])


    @classmethod
    def software_update_report(cls):
        try:
            f = open(os.path.join(cls.home_dir(), cls.__SCS_DIR, cls.__LATEST_UPDATE))
            report = f.read().strip()
            f.close()

            return report

        except FileNotFoundError:
            return None


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def gps_device(cls):
        return cls.__GPS_SERIAL_DEVICE


    @classmethod
    def ndir_usb_device(cls):
        return cls.__NDIR_USB_DEVICE            # we might have to search for it instead


    @classmethod
    def psu_device(cls):
        raise NotImplementedError()


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def name(cls):
        return socket.gethostname()


    @classmethod
    def server_ipv4_address(cls):
        return IPv4Address.construct(cls.__SERVER_ADDRESS)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def ndir_spi_bus(cls):
        return cls.__NDIR_SPI_BUS


    @classmethod
    def ndir_spi_device(cls):
        return cls.__NDIR_SPI_DEVICE


    @classmethod
    def opc_spi_bus(cls):
        return cls.__OPC_SPI_BUS


    @classmethod
    def opc_spi_device(cls):
        return cls.__OPC_SPI_DEVICE


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def disk_usage(cls, volume):
        st = os.statvfs(volume)

        free = st.f_bavail * st.f_frsize
        used = (st.f_blocks - st.f_bfree) * st.f_frsize
        total = st.f_blocks * st.f_frsize

        return DiskUsage(volume, free, used, total)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def time_is_synchronized(cls):
        return Path(cls.__TIME_SYNCHRONIZED).exists()               # TODO: test whether this works with an RTC


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def home_dir(cls):
        return os.environ[cls.OS_ENV_PATH] if cls.OS_ENV_PATH in os.environ else cls.__DEFAULT_HOME_DIR


    @classmethod
    def lock_dir(cls):
        return cls.__LOCK_DIR


    @classmethod
    def tmp_dir(cls):
        return cls.__TMP_DIR


    @classmethod
    def scs_dir(cls):
        return os.path.join(cls.home_dir(), cls.__SCS_DIR)


    @classmethod
    def command_dir(cls):
        return os.path.join(cls.home_dir(), cls.__SCS_DIR, cls.__COMMAND_DIR)


    @classmethod
    def conf_dir(cls):
        return os.path.join(cls.home_dir(), cls.__SCS_DIR, cls.__CONF_DIR)


    @classmethod
    def aws_dir(cls):
        return os.path.join(cls.home_dir(), cls.__SCS_DIR, cls.__AWS_DIR)


    @classmethod
    def osio_dir(cls):
        return os.path.join(cls.home_dir(), cls.__SCS_DIR, cls.__OSIO_DIR)


    @classmethod
    def eep_image(cls):
        return os.path.join(cls.home_dir(), cls.__SCS_DIR, cls.__DFE_EEP_IMAGE)
