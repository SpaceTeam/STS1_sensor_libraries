import os

import pytest

from sts1_sensor_libraries import ADXL345

def test_class_creation1():
    ADXL345()
    
def test_class_creation2():
    ADXL345(range=2, datarate=50)

def test_class_creation3():
    ADXL345(x_offset=-0.06, y_offset=0.03, z_offset=0.06)

def test_class_creation4():
    from smbus2 import SMBus
    with SMBus(1) as bus:
        ADXL345(bus=bus)

def test_class_creation5():
    ADXL345(address=0x53)

def test_class_creation6():
    os.environ["STS1_SENSOR_ADDRESS_AVXL345"] = "0x53"
    ADXL345()
    del os.environ["STS1_SENSOR_ADDRESS_AVXL345"]

def test_get_g():
    accel = ADXL345()
    accel.get_g()

def test_get_g_raw():
    accel = ADXL345()
    accel.get_g_raw()

def test_multiple_objects():
    a1 = ADXL345(address=0x53)
    a2 = ADXL345(address=0x53)
    a3 = ADXL345(address=0x53)
    for _ in range(5):
        a1.get_g()
        a2.get_g()
        a3.get_g()

def test_set_wrong_address1():
    with pytest.raises(ValueError):
        ADXL345(address=0x99)

def test_set_wrong_address2():
    with pytest.raises(ValueError):
        os.environ["STS1_SENSOR_ADDRESS_AVXL345"] = "0x98"
        ADXL345()
        del os.environ["STS1_SENSOR_ADDRESS_AVXL345"]

def test_set_wrong_datarate():
    with pytest.raises(ValueError):
        ADXL345(datarate=1337)

def test_set_wrong_range():
    with pytest.raises(ValueError):
        ADXL345(range=42)
