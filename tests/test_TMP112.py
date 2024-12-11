import pytest

from sts1_sensor_libraries import TMP112

def test_class_creation1():
    TMP112()

def test_class_creation2():
    TMP112(address=0x48, conversion_rate=1)

def test_class_creation3():
    TMP112(address=0x48, conversion_rate=4)

def test_class_creation4():
    TMP112(address=0x48, conversion_rate=4, extended_temp_range=True)

def test_class_creation5():
    TMP112(address=0x48, extended_temp_range=False)

def test_class_creation6():
    from smbus2 import SMBus
    with SMBus(1) as bus:
        TMP112(bus=bus, address=0x48)

def test_get_temp():
    t = TMP112(address=0x48, conversion_rate=1)
    t.get_temp()

def test_set_wrong_address():
    with pytest.raises(ValueError):
        TMP112(address=0x99)
