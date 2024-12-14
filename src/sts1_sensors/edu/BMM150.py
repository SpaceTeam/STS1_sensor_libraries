import math
import os
import time

import bmm150

from sts1_sensors.utils.PatchedSMBus import PatchedSMBus

class BMM150:
    """Geomagnetic sensor.

    Datasheet: https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmm150-ds001.pdf
    """
    def __init__(self, address=None, bus=None):
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
        return self.bmm.read_raw_mag_data()

    def get_magnetic_data(self):
        return self.bmm.read_mag_data()
    
    def get_heading(self):
        x, y, _ = self.get_magnetic_data()
        return math.degrees(math.atan2(x, y))
