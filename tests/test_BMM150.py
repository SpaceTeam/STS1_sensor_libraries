import os

import pytest

from sts1_sensors import BMM150

def test_class_creation1():
    BMM150()
    
def test_class_creation5():
    BMM150(address=0x10)

def test_class_creation6():
    os.environ["STS1_SENSOR_ADDRESS_BMM150"] = "0x10"
    BMM150()
    del os.environ["STS1_SENSOR_ADDRESS_BMM150"]

def test_get_values1():
    mag = BMM150()
    mag.get_raw_magnetic_data()

def test_get_values2():
    mag = BMM150()
    mag.get_magnetic_data()

def test_get_values3():
    mag = BMM150()
    mag.get_heading()

def test_set_wrong_address1():
    with pytest.raises(ValueError):
        BMM150(address=0x99)

def test_set_wrong_address2():
    with pytest.raises(ValueError):
        os.environ["STS1_SENSOR_ADDRESS_BMM150"] = "0x98"
        BMM150()
        del os.environ["STS1_SENSOR_ADDRESS_BMM150"]
