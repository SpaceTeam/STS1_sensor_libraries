import os

import pytest

from sts1_sensors import L3GD20H

def test_class_creation1():
    L3GD20H()

def test_class_creation2():
    L3GD20H(range=245, datarate=12.5)

def test_class_creation3():
    L3GD20H(range=2000)

def test_class_creation4():
    L3GD20H(datarate=800)

def test_class_creation5():
    from smbus2 import SMBus
    with SMBus(1) as bus:
        L3GD20H(bus=bus)

def test_class_creation6():
    os.environ["STS1_SENSOR_ADDRESS_L3GD20H"] = "0x6A"
    L3GD20H()
    del os.environ["STS1_SENSOR_ADDRESS_L3GD20H"]

def test_get_angular_momentum1():
    t = L3GD20H()
    t.get_angular_momentum_raw()

def test_get_angular_momentum2():
    t = L3GD20H()
    t.get_angular_momentum()

def test_set_wrong_address1():
    with pytest.raises(ValueError):
        L3GD20H(address=0x99)

def test_set_wrong_address2():
    with pytest.raises(ValueError):
        os.environ["STS1_SENSOR_ADDRESS_L3GD20H"] = "0x98"
        L3GD20H()
        del os.environ["STS1_SENSOR_ADDRESS_L3GD20H"]
