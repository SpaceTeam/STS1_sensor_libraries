import os

import pytest

from sts1_sensors import TMP112

def test_class_creation1():
    TMP112()

def test_class_creation2():
    TMP112(conversion_rate=4)

def test_class_creation3():
    TMP112(conversion_rate=4, extended_temp_range=False)

def test_class_creation4():
    TMP112(extended_temp_range=False)

def test_class_creation5():
    from smbus2 import SMBus
    with SMBus(1) as bus:
        TMP112(bus=bus, address=0x48)

def test_class_creation6():
    os.environ["STS1_SENSOR_ADDRESS_TMP112"] = "0x48"
    TMP112()
    del os.environ["STS1_SENSOR_ADDRESS_TMP112"]


def test_get_temperature():
    t = TMP112(address=0x48, conversion_rate=1)
    t.get_temperature()

def test_set_wrong_address1():
    with pytest.raises(ValueError):
        TMP112(address=0x99)

def test_set_wrong_address2():
    with pytest.raises(ValueError):
        os.environ["STS1_SENSOR_ADDRESS_TMP112"] = "0x98"
        TMP112()
        del os.environ["STS1_SENSOR_ADDRESS_TMP112"]
