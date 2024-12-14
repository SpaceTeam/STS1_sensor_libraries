import os

import pytest

from sts1_sensors import BME688

def test_class_creation1():
    BME688()
    
def test_class_creation5():
    BME688(address=0x76)

def test_class_creation6():
    os.environ["STS1_SENSOR_ADDRESS_BME688"] = "0x76"
    BME688()
    del os.environ["STS1_SENSOR_ADDRESS_BME688"]

def test_get_values1():
    s = BME688()
    s.get_temperature()
    
def test_get_values2():
    s = BME688()
    s.get_pressure()

def test_get_values3():
    s = BME688()
    s.get_humidity()

def test_get_values4():
    s = BME688(enable_gas_measurements=True)
    s.get_heat_stable()

def test_get_values5():
    s = BME688(enable_gas_measurements=True)
    s.get_gas_resistance()

def test_get_values6():
    s = BME688(enable_gas_measurements=True)
    s.get_all_data()

def test_set_values1():
    s = BME688()
    s.enable_gas_measurements = True
    s.gas_heater_temperature = 320
    s.gas_heater_duration = 150

def test_set_wrong_address1():
    with pytest.raises(ValueError):
        BME688(address=0x99)

def test_set_wrong_address2():
    with pytest.raises(ValueError):
        os.environ["STS1_SENSOR_ADDRESS_BME688"] = "0x98"
        BME688()
        del os.environ["STS1_SENSOR_ADDRESS_BME688"]
