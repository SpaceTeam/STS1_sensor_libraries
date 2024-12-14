import math
import os
import time

import bmm150

from sts1_sensors.utils.PatchedSMBus import PatchedSMBus

class BMM150:
    """Geomagnetic sensor.
    """

    def __init__(self, address=None, bus=None):
        """Geomagnetic sensor.

        Builds on top of the library `bmm150 <https://gitlab.com/umoreau/bmm150>`_.

        :param hexadecimal address: Physical address of the sensor on the board (see `i2cdetect` command). Allowed values: `[0x10, 0x11, 0x12, 0x13]`. If None, the environment variable `STS1_SENSOR_ADDRESS_BMM150` will be used. If environment variable is not found, 0x10 will be used.
        :param SMBus bus: A SMBus object. If None, this class will generate its own, defaults to None.
        
        Example:

        .. code-block:: python

           mag = BMM150()
           x, y, z = mag.get_magnetic_data()
           print(f"{x=:.2f} µT, {y=:.2f} µT, {z=:.2f} µT")
           print(f"Heading: {mag.get_heading():.2f}°")
        """
        self.possible_addresses = [0x10, 0x11, 0x12, 0x13]
        a = address or int(os.environ.get("STS1_SENSOR_ADDRESS_BMM150", "0x10"), 16)

        self.address = a
        self.bus = PatchedSMBus(address=a, bus=bus)

        self.bmm = bmm150.BMM150(auto_init=False)
        self.bmm.i2c_bus = self.bus
        self.bmm.initialize()
    
        # Wait up to 10 secs for sensor to be ready
        for _ in range(20):
            if self.bus.read_byte_data(0, 0x48) & 1 == 1:
                break
            time.sleep(0.5)

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
        
    def get_raw_magnetic_data(self):
        """Get raw magnetic data in µT.
        """
        return self.bmm.read_raw_mag_data()

    def get_magnetic_data(self):
        """Get magnetic data in µT.
        """
        return self.bmm.read_mag_data()
    
    def get_heading(self):
        """Get heading direction in degrees. Uses only x and y for calculation (z is ignored).
        """
        x, y, _ = self.get_magnetic_data()
        return math.degrees(math.atan2(x, y))
