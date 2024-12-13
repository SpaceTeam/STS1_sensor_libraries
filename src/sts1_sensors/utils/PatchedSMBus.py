import os

from smbus2 import SMBus

class PatchedSMBus:
    def __init__(self, address, bus=None):
        self.address = address
        
        if bus is None:
            self.manage_bus = True
            self.bus = SMBus(int(os.environ.get("STS1_SENSORS_I2C_BUS_ADDRESS", 1)))
        else:
            self.manage_bus = False
            self.bus = bus

    def __del__(self):
        if self.manage_bus:
            self.bus.close()

    def read_byte_data(self, ignored, *args, **kwargs):
        return self.bus.read_byte_data(self.address, *args, **kwargs)

    def write_byte_data(self, ignored, *args, **kwargs):
        return self.bus.write_byte_data(self.address, *args, **kwargs)

    def read_i2c_block_data(self, ignored, *args, **kwargs):
        return self.bus.read_i2c_block_data(self.address, *args, **kwargs)
