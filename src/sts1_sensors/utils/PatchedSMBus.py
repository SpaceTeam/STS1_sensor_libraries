from smbus2 import SMBus

class PatchedSMBus:
    def __init__(self, bus_number, address):
        self.bus = SMBus(bus_number)
        self.address = address

    def read_byte_data(self, ignored, *args, **kwargs):
        return self.bus.read_byte_data(self.address, *args, **kwargs)

    def write_byte_data(self, ignored, *args, **kwargs):
        return self.bus.write_byte_data(self.address, *args, **kwargs)

    def read_i2c_block_data(self, ignored, *args, **kwargs):
        return self.bus.read_i2c_block_data(self.address, *args, **kwargs)

    def __del__(self):
        self.bus.close()
