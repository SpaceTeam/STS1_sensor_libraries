import os

from sts1_sensors.utils.AbstractSensor import AbstractSensor
from sts1_sensors.utils.utils import twos_comp

class L3GD20H(AbstractSensor):
    """Three-axis gyroscope
    """
    _possible_ranges = [245, 500, 2000]
    _possible_datarates = [12.5, 25, 50, 100, 200, 400, 800]
    _possible_datarates_bin = [(0, 1), (1, 1), (2, 1), (0, 0), (1, 0), (2, 0), (3, 0)]
    
    def __init__(self, range=245, datarate=12.5, address=None, bus=None):
        """Three-axis gyroscope.

        :param int range: Maximum angular velocity or speed of rotation that the gyro can read, measured in degrees per second (dps). Allowed values: `[245, 500, 2000]`, defaults to 245.
        :param float datarate: Number of measurements per second [Hz]. Allowed values: `[12.5, 25, 50, 100, 200, 400, 800]`, defaults to 12.5.
        :param hexadecimal address: Physical address of the sensor on the board (see `i2cdetect` command). Allowed values: `[0x6A, 0x6B]`. If None, the environment variable `STS1_SENSOR_ADDRESS_L3GD20H` will be used. If environment variable is not found, 0x6A will be used.
        :param SMBus bus: A SMBus object. If None, this class will generate its own, defaults to None.
        
        Example:

        .. code-block:: python

           gyro = L3GD20H(range=245, datarate=12.5)
           x, y, z = gyro.get_angular_momentum()
           print(f"{x=:.2f} dps, {y=:.2f} dps, {z=:.2f} dps")
        """
        super().__init__(possible_addresses=[0x6A, 0x6B], bus=bus)

        self.address = address or int(os.environ.get("STS1_SENSOR_ADDRESS_L3GD20H", "0x6A"), 16)
        self.range = range
        self.datarate = datarate
        self.xyz_addresses = {"x": 0x28, "y": 0x2A, "z": 0x2C}
        self.dps_per_digit = [0.00875, 0.01750, 0.07000]

        # write CTRL1 datarate, bandwith, powermode and enable for all axis
        # write CTRL4 Block Data update, Big/little endian, Full Scale Selection,
        # write LOW_ODR
        a, b = self._possible_datarates_bin[self._possible_datarates.index(self.datarate)]
        self.bus.write_byte_data(self.address, 0x20, 0b1111 | (a << 6))
        self.bus.write_byte_data(self.address, 0x23, (self._possible_ranges.index(self.range) << 4))
        self.bus.write_byte_data(self.address, 0x39, b)

    @property
    def datarate(self):
        return self._datarate

    @datarate.setter
    def datarate(self, datarate):
        if datarate not in self._possible_datarates:
            s = f"The datarate {datarate} does not exist."
            s += f" Choose one of {self._possible_datarates}."
            raise ValueError(s)
        self._datarate = datarate

    @property
    def range(self):
        return self._range

    @range.setter
    def range(self, range):
        if range not in self._possible_ranges:
            s = f"The range {range} does not exist."
            s += f" Choose one of {self._possible_ranges}."
            raise ValueError(s)
        self._range = range

    def _get_raw(self, var):
        lsb, msb = self.bus.read_i2c_block_data(self.address, self.xyz_addresses[var], 2)
        return twos_comp((msb << 8) + lsb, 16)

    def get_angular_momentum_raw(self):
        "Get raw degrees per second."
        return self._get_raw("x"), self._get_raw("y"), self._get_raw("z")

    def _get_angular_momentum(self, var):
        k = self._get_raw(var)
        return k * self.dps_per_digit[self._possible_ranges.index(self.range)]

    def get_angular_momentum(self):
        "Get degrees per second."
        return self._get_angular_momentum("x"), self._get_angular_momentum("y"), self._get_angular_momentum("z")
