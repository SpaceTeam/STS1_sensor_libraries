import os

from smbus2 import i2c_msg

from sts1_sensors.utils.AbstractSensor import AbstractSensor

class TMP112(AbstractSensor):
    """High-accuracy temperature sensor.
    """
    _possible_conversion_rates = [0.25, 1, 4, 8]
    
    def __init__(self, conversion_rate=1, extended_temp_range=True, address=None, bus=None):
        """High-accuracy temperature sensor.

        :param int conversion_rate: Conversion rate. Allowed values: `[0.25, 1, 4, 8]`. Defaults to 1. 
        :param bool extended_temp_range: If True, range: -55°C - 150°C, if False range: -55°C - 128°C, defaults to True.
        :param hexadecimal address: Physical address of the sensor on the board (see `i2cdetect` command). Allowed values: `[0x48, 0x49, 0x4A, 0x4B]`. If None, the environment variable `STS1_SENSOR_ADDRESS_TMP112` will be used. If environment variable is not found, 0x48 will be used.
        :param SMBus bus: A SMBus object. If None, this class will generate its own, defaults to None.
                
        Example:

        .. code-block:: python

           temp = TMP112(conversion_rate=1, extended_temp_range=True)
           print(f"{temp.get_temperature():.2f} °C")
        """
        super().__init__(possible_addresses=[0x48, 0x49, 0x4A, 0x4B], bus=bus)

        self.address = address or int(os.environ.get("STS1_SENSOR_ADDRESS_TMP112", "0x48"), 16)
        self.conversion_rate = conversion_rate
        self.extended_temp_range = extended_temp_range
        
        c = self._possible_conversion_rates.index(self.conversion_rate)
        m = int(self.extended_temp_range)
        self.bus.i2c_rdwr(i2c_msg.write(self.address, [0b1,0b1100000,0b100000 + (c << 6) + (m << 4)]))

    @property
    def conversion_rate(self):
        return self._conversion_rate

    @conversion_rate.setter
    def conversion_rate(self, conversion_rate):
        if conversion_rate not in self._possible_conversion_rates:
            s = f"The conversion_rate {conversion_rate} does not exist."
            s += f" Choose one of {self._possible_conversion_rates}."
            raise ValueError(s)
        self._conversion_rate = conversion_rate

    def get_temperature(self):
        """Get temperature in Celcius."""
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
