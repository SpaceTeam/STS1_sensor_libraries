import os

import pytest

from sts1_sensors import BME688

def test_class_creation1():
    BME688()
    
def test_class_creation2():
    BME688(temperature_osr=2, humidity_osr=4, pressure_osr=8)

def test_class_creation3():
    BME688(use_gas=False)

def test_class_creation4():
    from smbus2 import SMBus
    with SMBus(1) as bus:
        BME688(bus=bus)

def test_class_creation5():
    BME688(address=0x76)

def test_class_creation6():
    os.environ["STS1_SENSOR_ADDRESS_BME688"] = "0x76"
    BME688()
    del os.environ["STS1_SENSOR_ADDRESS_BME688"]

def test_get_values1():
    accel = BME688(use_gas=True)
    accel.get_values()

def test_get_values2():
    accel = BME688(use_gas=False)
    accel.get_values()

def test_set_wrong_address1():
    with pytest.raises(ValueError):
        BME688(address=0x99)

def test_set_wrong_address2():
    with pytest.raises(ValueError):
        os.environ["STS1_SENSOR_ADDRESS_BME688"] = "0x98"
        BME688()
        del os.environ["STS1_SENSOR_ADDRESS_BME688"]

def test_set_wrong_gas_temperature():
    with pytest.raises(ValueError):
        BME688(gas_temperature=500)

def test_set_wrong_gas_time1():
    with pytest.raises(ValueError):
        BME688(gas_time=0)

def test_set_wrong_gas_time2():
    with pytest.raises(ValueError):
        BME688(gas_time=4500)


