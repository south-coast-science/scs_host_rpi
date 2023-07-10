"""
Created on 16 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://raspberrypi.stackexchange.com/questions/2086/how-do-i-get-the-serial-number
"""

import os
import re
import socket

from pathlib import Path
from subprocess import check_output, call, Popen, PIPE, DEVNULL

from scs_core.estate.git_pull import GitPull

from scs_core.sys.disk_usage import DiskUsage
from scs_core.sys.disk_volume import DiskVolume
from scs_core.sys.ipv4_address import IPv4Address
from scs_core.sys.network import Networks
from scs_core.sys.node import IoTNode
from scs_core.sys.persistence_manager import FilesystemPersistenceManager
from scs_core.sys.uptime_datum import UptimeDatum

from scs_host.sys.host_status import HostStatus


# --------------------------------------------------------------------------------------------------------------------

class Host(IoTNode, FilesystemPersistenceManager):
    """
    Broadcom BCM2837 64bit ARMv7 quad core processor
    """

    OS_ENV_PATH =           'SCS_ROOT_PATH'

    I2C_EEPROM =            3
    I2C_APPLICATION =       1

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

    __LATEST_UPDATE =       "latest_update.txt"                 # hard-coded rel path
    __DFE_EEP_IMAGE =       "dfe_cape.eep"                      # hard-coded rel path


    # ----------------------------------------------------------------------------------------------------------------
    # host acting as DHCP server...

    __SERVER_IPV4_ADDRESS = '172.22.15.1'                       # had-coded abs path


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
        call(['sudo', 'dtoverlay', 'i2c-gpio', 'i2c_gpio_sda=0', 'i2c_gpio_scl=1'])


    @staticmethod
    def shutdown():
        call(['systemctl', 'poweroff', '-i'])


    @classmethod
    def software_update_report(cls):
        git_pull = GitPull.load(cls)

        return None if git_pull is None else str(git_pull.pulled_on.datetime.date())


    # ----------------------------------------------------------------------------------------------------------------
    # network identity...

    @classmethod
    def name(cls):
        return socket.gethostname()


    @classmethod
    def server_ipv4_address(cls):
        return IPv4Address.construct(cls.__SERVER_IPV4_ADDRESS)


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
    # status...

    @classmethod
    def status(cls):
        message = str(os.popen("vcgencmd measure_temp").readline())
        message = message.replace("temp=", "").replace("'C\n", "")

        temp = float(message)

        return HostStatus(temp)


    # ----------------------------------------------------------------------------------------------------------------
    # networks and modem...

    @classmethod
    def networks(cls):
        p = Popen(['nmcli', 'd'], stdout=PIPE, stderr=DEVNULL)
        stdout, _ = p.communicate(timeout=10)

        if p.returncode != 0:
            return None

        return Networks.construct_from_nmcli(stdout.decode().splitlines())


    @classmethod
    def modem(cls):
        return None


    @classmethod
    def modem_conn(cls):
        return None


    @classmethod
    def sim(cls):
        return None


    # ----------------------------------------------------------------------------------------------------------------
    # SPI...

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
    def disk_volume(cls, mounted_on):
        process = Popen(['df'], stdout=PIPE)
        out, _ = process.communicate()
        rows = out.decode().splitlines()[1:]

        for row in rows:
            volume = DiskVolume.construct_from_df_row(row)

            if volume.mounted_on == mounted_on:
                return volume

        return None


    @classmethod
    def disk_usage(cls, path):
        try:
            st = os.statvfs(path)

        except OSError:
            return None

        return DiskUsage.construct_from_statvfs(path, st)


    # ----------------------------------------------------------------------------------------------------------------
    # SPI...

    @classmethod
    def opc_spi_dev_path(cls):
        return None


    @classmethod
    def ndir_spi_dev_path(cls):
        return None


    # ----------------------------------------------------------------------------------------------------------------
    # time...

    @classmethod
    def time_is_synchronized(cls):
        return Path(cls.__TIME_SYNCHRONIZED).exists()


    @classmethod
    def uptime(cls, now=None):
        raw = check_output('uptime')
        report = raw.decode()

        return UptimeDatum.construct_from_report(now, report)


    # ----------------------------------------------------------------------------------------------------------------
    # tmp directories...

    @classmethod
    def lock_dir(cls):
        return cls.__LOCK_DIR


    @classmethod
    def tmp_dir(cls):
        return cls.__TMP_DIR


    # ----------------------------------------------------------------------------------------------------------------
    # filesystem paths...

    @classmethod
    def home_path(cls):
        return os.environ[cls.OS_ENV_PATH] if cls.OS_ENV_PATH in os.environ else cls.__DEFAULT_HOME_DIR


    @classmethod
    def scs_path(cls):
        return os.path.join(cls.home_path(), cls.__SCS_DIR)


    @classmethod
    def command_path(cls):
        return os.path.join(cls.scs_path(), cls.__COMMAND_DIR)


    @classmethod
    def eep_image(cls):
        return os.path.join(cls.scs_path(), cls.__DFE_EEP_IMAGE)
