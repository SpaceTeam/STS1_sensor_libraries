import os

from smbus2 import SMBus

class AbstractSensor:
    def __init__(self, possible_addresses, bus=None):
        self.possible_addresses = possible_addresses

        if bus is None:
            self.manage_bus = True
            self.bus = SMBus(int(os.environ.get("STS1_SENSORS_I2C_BUS_ADDRESS", 1)))
        else:
            self.manage_bus = False
            self.bus = bus

    def __del__(self):
        if self.manage_bus:
            self.bus.close()

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
