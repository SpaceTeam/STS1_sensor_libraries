import math
import os
import time

import bmm150

from sts1_sensors.utils.AbstractSensor import AbstractSensor
from sts1_sensors.utils.PatchedSMBus import PatchedSMBus


class BMM150(AbstractSensor):
    """Geomagnetic sensor.

    Datasheet: https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmm150-ds001.pdf
    """
    def __init__(self, address=None):
        a = address or int(os.environ.get("STS1_SENSOR_ADDRESS_BMM150", "0x10"), 16)
        bus = PatchedSMBus(int(os.environ.get("STS1_SENSORS_I2C_BUS_ADDRESS", 1)), address=a)
        super().__init__(possible_addresses=[0x10, 0x11, 0x12, 0x13], bus=bus)

        self.address = a

        self.bmm = bmm150.BMM150(auto_init=False)
        self.bmm.i2c_bus = self.bus
        self.bmm.initialize()
    
        # Wait up to 10 secs for sensor to be ready
        for _ in range(20):
            if self.bus.read_byte_data(0, 0x48) & 1 == 1:
                break
            time.sleep(0.5)

    def get_raw_magnetic_data(self):
        return self.bmm.read_raw_mag_data()

    def get_magnetic_data(self):
        return self.bmm.read_mag_data()
    
    def get_heading(self):
        x, y, _ = self.get_magnetic_data()
        return math.degrees(math.atan2(x, y))
