import math

import bmm150

# import bmm150.bmm150_defs

# import mock
from smbus2 import SMBus

# with mock.patch("bmm150.bmm150_defs.BMM150_I2C_Address", 0x10):

# bmm150.BMM150_I2C_Address = 0x10
bmm150.bmm150_defs.BMM150_I2C_Address = 0x10
# __import__('bmm150', dict(BMM150_I2C_Address=0x10, **globals()))

class PatchedSMBus:

    def __init__(self, bus_number):
        self.bus = SMBus(bus_number)

    def read_byte_data(self, ignored, *args, **kwargs):
        return self.bus.read_byte_data(0x10, *args, **kwargs)

    def write_byte_data(self, ignored, *args, **kwargs):
        return self.bus.write_byte_data(0x10, *args, **kwargs)

    def read_i2c_block_data(self, ignored, *args, **kwargs):
        return self.bus.read_i2c_block_data(0x10, *args, **kwargs)


bmm = bmm150.BMM150(auto_init=False)
bmm.i2c_bus = PatchedSMBus(1)
bmm.initialize()

x, y, z = bmm.read_mag_data()

heading_rads = math.atan2(x, y)

heading_degrees = math.degrees(heading_rads)

print(f"X : {x:.2f}µT")
print(f"Y : {y:.2f}µT")
print(f"Z : {z:.2f}µT")

print(f"Heading: {heading_degrees:.2f}°")
