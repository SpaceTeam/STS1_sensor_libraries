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

def test_preset_modes():
    BMM150(preset_mode=1)
    BMM150(preset_mode=2)
    BMM150(preset_mode=3)
    BMM150(preset_mode=4)

def test_set_wrong_preset_mode():
    with pytest.raises(ValueError):
        BMM150(preset_mode=5)

def test_set_wrong_address1():
    with pytest.raises(ValueError):
        BMM150(address=0x99)

def test_set_wrong_address2():
    with pytest.raises(ValueError):
        os.environ["STS1_SENSOR_ADDRESS_BMM150"] = "0x98"
        BMM150()
        del os.environ["STS1_SENSOR_ADDRESS_BMM150"]
