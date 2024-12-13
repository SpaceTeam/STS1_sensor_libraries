import os
import time

from sts1_sensors.sensors.AbstractSensor import AbstractSensor

class BMM150(AbstractSensor):
    """Geomagnetic sensor.
    """
    _possible_datarates = [1, 2, 6, 8, 15, 20, 25, 30]
    
    def __init__(self, datarate=8, address=None, bus=None):
        super().__init__(possible_addresses=[0x10, 0x11, 0x12, 0x13], bus=bus)

        self.address = address or int(os.environ.get("STS1_SENSOR_ADDRESS_BMM150", "0x10"), 16)
        self.datarate = datarate
        self.xyz_addresses = {"x": 0x42, "y": 0x44, "z": 0x46}

        self.bus.write_byte_data(self.addr, 0x4B, 1)
        time.sleep(1)
        self.bus.write_byte_data(self.addr, 0x4C, self.poss_datarate.index(self.datarate) << 3)
        self.bus.write_byte_data(self.addr, 0x51, 0b1111)
        self.bus.write_byte_data(self.addr, 0x52, 0b1111)

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
        

    def _get_raw(self, var):
        lsb, msb = self.bus.read_i2c_block_data(self.address, self.xyz_addresses[var], 2)
        k = (msb << 8) | lsb
        k = k >> 3

        if var in ("x", "y"):
            shift = 12
        elif var == "z":
            shift = 15

        if (k >> shift) == 1:
            k = (1 << shift) - (k & 0b111111111111111)
            k = k * (-1)                
        return k
    
    def get_raw(self):
        return self._get_raw("x"), self._get_raw("y"), self._get_raw("z")

    def _get_ut(self, var):
        lsb, msb = self.bus.read_i2c_block_data(self.address, self.xyz_addresses[var], 2)
        k = (msb << 8) | lsb
        k = k >> 3

        if var in ("x", "y"):
            shift = 12
        elif var == "z":
            shift = 14

        if (k >> shift) == 1:
            k = k - (1 << (shift+1))

        if var in ("x", "y"):
            return k / 3.15076
        elif var == "z":
            return k / 6.5536 

    def get_ut(self):
        return self._get_ut("x"), self._get_ut("y"), self._get_ut("z")
