import os

from sts1_sensor_libraries.AbstractSensor import AbstractSensor

class ADXL345(AbstractSensor):
    """Digital accelerometer.
    """
    _possible_addresses = [0x1D, 0x3A, 0x3B, 0x53]
    _possible_datarates = [0.10, 0.20, 0.39, 0.78, 1.56, 3.13, 6.25, 12.5, 25, 50, 100, 200, 400, 800, 1600, 3200]
    _possible_ranges = [2, 4, 8, 16]

    def __init__(self, range=2, datarate=50, x_offset=0, y_offset=0, z_offset=0, address=None, bus=None):
        """Digital accelerometer.

        :param int range: How many gs the sensor should be able measure. Allowed values: `[2, 4, 8, 16]`. Defaults to 2.
        :param int datarate: How often the sensor should measure in Hz. Allowed values: `[0.10, 0.20, 0.39, 0.78, 1.56, 3.13, 6.25, 12.5, 25, 50, 100, 200, 400, 800, 1600, 3200]`. Defaults to 50.
        :param int x_offset: x-axis offset, defaults to 0.
        :param int y_offset: y-axis offset, defaults to 0.
        :param int z_offset: z-axis offset, defaults to 0.
        :param hexadecimal address: Physical address of the sensor on the board (see `i2cdetect` command). Allowed values: `[0x1D, 0x3A, 0x3B, 0x53]`. If None, the environment variable `STS1_SENSOR_ADDRESS_AVXL345` will be used. If environment variable is not found, 0x53 will be used.
        :param SMBus bus: A SMBus object. If None, this class will generate its own, defaults to None.
        
        :meta public:
        """
        super().__init__(bus)
            
        self.address = address or int(os.environ.get("STS1_SENSOR_ADDRESS_AVXL345", "0x53"), 16)
        self.datarate = datarate
        self.range = range
        self.offsets = {"x": x_offset, "y": y_offset, "z": z_offset}
        self.xyz_addresses = {"x": 0x32, "y": 0x34, "z": 0x36}

        self.bus.write_byte_data(self.address, 0x2C, self._possible_datarates.index(self.datarate))
        self.bus.write_byte_data(self.address, 0x2D, 0b1000)
        self.bus.write_byte_data(self.address, 0x31, 0b1011 & self._possible_ranges.index(self.range))

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        if address not in self._possible_addresses:
            s = f"The address {hex(address)} does not exist."
            s += f" Choose one of {self._possible_addresses}."
            raise ValueError(s)
        self._address = address

    @property
    def datarate(self):
        return self._datarate

    @datarate.setter
    def datarate(self, datarate):
        if datarate not in self._possible_datarates:
            s = f"The datarate {hex(datarate)} does not exist."
            s += f" Choose one of {self._possible_datarates}."
            raise ValueError(s)
        self._datarate = datarate

    @property
    def range(self):
        return self._range

    @range.setter
    def range(self, range):
        if range not in self._possible_ranges:
            s = f"The range {hex(range)} does not exist."
            s += f" Choose one of {self._possible_ranges}."
            raise ValueError(s)
        self._range = range

    def _get_g_raw(self, var):
        lsb, msb = self.bus.read_i2c_block_data(self.address, self.xyz_addresses[var], 2)
        k = (msb << 8) | lsb
        if (k >> 15) == 1:
            k = (1 << 15) - (k & 0b111111111111111)
            k = k * (-1)                
        return k
    
    def get_g_raw(self):
        """Get raw acceleration.
        """
        return self._get_g_raw("x"), self._get_g_raw("y"), self._get_g_raw("z")
    
    def _get_g(self, var):
        k = self._get_g_raw(var)
        k = (k / (0b111111111)) * self.range
        k = k + self.offsets[var]
        return k

    def get_g(self):
        """Get acceleration adjusted by previously defined offsets.
        """
        return self._get_g("x"), self._get_g("y"), self._get_g("z")
