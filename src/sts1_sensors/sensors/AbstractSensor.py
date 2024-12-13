import os

from smbus2 import SMBus

class AbstractSensor:
    def __init__(self, bus=None):
        if bus is None:
            self.manage_bus = True
            self.bus = SMBus(int(os.environ.get("STS1_SENSORS_I2C_BUS_ADDRESS", 1)))
        else:
            self.manage_bus = False
            self.bus = bus

    def __del__(self):
        if self.manage_bus:
            self.bus.close()
