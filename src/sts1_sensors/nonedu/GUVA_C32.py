import os
from smbus2 import i2c_msg

from sts1_sensors.utils.AbstractSensor import AbstractSensor

class GUVA_C32(AbstractSensor):
    """Ultraviolet light sensor.
    """
    _possible_resolutions = [800, 400, 200, 100]
    _possible_ranges = [1, 2, 4, 8, 16, 32, 64, 128]
    
    def __init__(self, range=1, resolution=800, address=None, bus=None):
        super().__init__(possible_addresses=[0x39], bus=bus)

        self.address = address or int(os.environ.get("STS1_SENSOR_ADDRESS_GUVA_C32", "0x39"), 16)
        self.range = range
        self.resolution = resolution

        #set power mode normal 0b00 and operation mode UVAoperation 0b01 -> 0b00010000 0x01
        msg = i2c_msg.write(self.addr, [0x01, 0b00010000])
        self.bus.i2c_rdwr(msg)
        #set resolution 0x04
        msg = i2c_msg.write(self.addr, [0x04, 0b00000011])
        #msg = i2c_msg.write(self.addr, [0x04, 0b00000000 + self.poss_res_bin[self.poss_res.index(self.res)]])
        self.bus.i2c_rdwr(msg)
        #set range  0x05
        msg = i2c_msg.write(self.addr, [0x05, 0b00000000])
        #msg = i2c_msg.write(self.addr, [0x05, 0b00000000 + self.poss_range_bin[self.poss_range.index(self.range_)]])
        self.bus.i2c_rdwr(msg)

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

    @property
    def resolution(self):
        return self._resolution

    @resolution.setter
    def resolution(self, resolution):
        if resolution not in self._possible_resolutions:
            s = f"The resolution {resolution} does not exist."
            s += f" Choose one of {self._possible_resolutions}."
            raise ValueError(s)
        self._resolution = resolution
            
    def getRawUVA(self):
        msg_w = i2c_msg.write(self.addr, [0x15])
        msg_r = i2c_msg.read(self.addr, 2)
        self.bus.i2c_rdwr(msg_w)
        self.bus.i2c_rdwr(msg_r)
        
        byte = []
        for value in msg_r:
            byte.append(value)
        
        return (byte[0] + (byte[1] << 8))
         
    def getUVA(self):
        return round(self.getRawUVA() / 4096)
