from smbus2 import i2c_msg

from sts1_sensor_libraries.AbstractSensor import AbstractSensor

class TMP112(AbstractSensor):
    """Temperature sensor.
    """
    possible_addresses = [0x48, 0x49, 0x4A, 0x4B]
    possible_conversion_rates = [0.25, 1, 4, 8]
    
    def __init__(self, bus=None, address=0x48, conversion_rate=1, extended_temp_range=True):
        """_summary_
        :param bool extended_temp_range: If true, range: -55°C - 150°C, if false range: -55°C - 128°C, defaults to True
        """
        super().__init__(bus)

        self.address = address
        self.conversion_rate = conversion_rate
        self.extended_temp_range = extended_temp_range
        
        c = self.possible_conversion_rates.index(self.conversion_rate)
        m = int(self.extended_temp_range)
        self.bus.i2c_rdwr(i2c_msg.write(self.address, [0b1,0b1100000,0b100000 + (c << 6) + (m << 4)]))

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        if address not in self.possible_addresses:
            s = f"The address {hex(address)} does not exist."
            s += f" Choose one of {self.possible_addresses}."
            raise ValueError(s)
        self._address = address

    @property
    def conversion_rate(self):
        return self._conversion_rate

    @conversion_rate.setter
    def conversion_rate(self, conversion_rate):
        if conversion_rate not in self.possible_conversion_rates:
            s = f"The conversion_rate {conversion_rate} does not exist."
            s += f" Choose one of {self.possible_conversion_rates}."
            raise ValueError(s)
        self._conversion_rate = conversion_rate

    def get_temp(self):
        msg_w = i2c_msg.write(self.address, [0])
        msg_r = i2c_msg.read(self.address, 2)
        self.bus.i2c_rdwr(msg_w)
        self.bus.i2c_rdwr(msg_r)
        
        byte = []
        for value in msg_r:
            byte.append(value)

        m = int(self.extended_temp_range)
        
        raw = ((byte[0] << 8) + byte[1]) >> (4-m)
        if (raw >> (11 + m)) == 1:
            raw = raw - (1 << (12 + m))
        temp = raw * 0.0625
        return temp
