
class ADXL345_new:
    possible_addresses = [0x1D, 0x3A, 0x3B, 0x53]
    possible_datarates = [0.10, 0.20, 0.39, 0.78, 1.56, 3.13, 6.25, 12.5, 25, 50, 100, 200, 400, 800, 1600, 3200]
    possible_ranges = [2, 4, 8, 16]

    def __init__(self, bus, address=0x53, range=2, datarate=3200, x_offset=0, y_offset=0, z_offset=0):
        self.bus = bus
        self.address = address
        self.datarate = datarate
        self.range = range
        self.offsets = {"x": x_offset, "y": y_offset, "z": z_offset}
        self.xyz_addresses = {"x": 0x32, "y": 0x34, "z": 0x36}

        self.bus.write_byte_data(self.address, 0x2C, bin(self.possible_datarates.index(self.datarate)))
        self.bus.write_byte_data(self.address, 0x2D, 0b1000)
        self.bus.write_byte_data(self.address, 0x31, 0b1011 & bin(self.possible_ranges.index(self.range)))

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        if address not in self.possible_addresses:
            raise ValueError(f"The address {hex(address)} does not exist.")
        self._address = address

    @property
    def datarate(self):
        return self._datarate

    @datarate.setter
    def datarate(self, datarate):
        if datarate not in self.possible_datarates:
            raise ValueError(f"The datarate {hex(datarate)} does not exist.")
        self._datarate = datarate

    @property
    def range(self):
        return self._range

    @range.setter
    def range(self, range):
        if range not in self.possible_ranges:
            raise ValueError(f"The range {hex(range)} does not exist.")
        self._range = range

    def _get_g_raw(self, var):
        lsb, msb = self.bus.read_i2c_block_data(self.address, self.xyz_addresses[var], 2)
        k = (msb << 8) | (lsb << 0)
        if (k >> 15) == 1:
            k = (1 << 15) - (k & 0b111111111111111)
            k = k * (-1)                
        return k
    
    def get_g_raw(self):
        return self._get_g_raw("x"), self._get_g_raw("y"), self._get_g_raw("z")
    
    def _get_g(self, var):
        k = self._get_g_raw(var)
        k = (k / (0b111111111)) * self.range
        k = k + self.offsets[var]
        return k

    def get_g(self):
        return self._get_g("x"), self._get_g("y"), self._get_g("z")
