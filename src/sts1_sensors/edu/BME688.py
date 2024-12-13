import os

import bme680 

from sts1_sensors.utils.AbstractSensor import AbstractSensor

class BME688(AbstractSensor):
    """Pressure, humidity, temperature and gas sensor.
    """
    # over-sampling rates
    _possible_temperature_osrs = [None, 1, 2, 4, 8, 16]
    _possible_humidity_osrs = [None, 1, 2, 4, 8, 16]
    _possible_pressure_osrs = [None, 1, 2, 4, 8, 16]
    _possible_iir_filter_sizes = [0, 1, 3, 7, 15, 31, 63, 127]

    def __init__(self, temperature_osr=8, humidity_osr=2, pressure_osr=4, iir_filter_size=3, 
                 temperature_offset=0, address=None, bus=None):
        super().__init__(possible_addresses=[0x76, 0x77], bus=bus)

        self.address = address or int(os.environ.get("STS1_SENSOR_ADDRESS_BME688", "0x76"), 16)
        self.bme680 = bme680.BME680(self.address, self.bus)

        self.temperature_osr = temperature_osr
        self.humidity_osr = humidity_osr
        self.pressure_osr = pressure_osr
        self.temperature_offset = temperature_offset
        self.iir_filter_size = iir_filter_size

    @property
    def temperature_osr(self):
        return self._temperature_osr

    @temperature_osr.setter
    def temperature_osr(self, temperature_osr):
        if temperature_osr not in self._possible_temperature_osrs:
            s = f"Unexpected temperature_osr {temperature_osr}."
            s += f" Choose one of {self._possible_temperature_osrs}."
            raise ValueError(s)
        self._temperature_osr = temperature_osr
        self.bme680.set_temperature_oversample(self._possible_temperature_osrs.index(temperature_osr))

    @property
    def humidity_osr(self):
        return self._humidity_osr

    @humidity_osr.setter
    def humidity_osr(self, humidity_osr):
        if humidity_osr not in self._possible_humidity_osrs:
            s = f"Unexpected humidity_osr {humidity_osr}."
            s += f" Choose one of {self._possible_humidity_osrs}."
            raise ValueError(s)
        self._humidity_osr = humidity_osr
        self.bme680.set_humidity_oversample(self._possible_humidity_osrs.index(humidity_osr))

    @property
    def pressure_osr(self):
        return self._pressure_osr

    @pressure_osr.setter
    def pressure_osr(self, pressure_osr):
        if pressure_osr not in self._possible_pressure_osrs:
            s = f"Unexpected pressure_osr {pressure_osr}."
            s += f" Choose one of {self._possible_pressure_osrs}."
            raise ValueError(s)
        self._pressure_osr = pressure_osr
        self.bme680.set_pressure_oversample(self._possible_pressure_osrs.index(pressure_osr))

    @property
    def iir_filter_size(self):
        return self._iir_filter_size

    @iir_filter_size.setter
    def iir_filter_size(self, iir_filter_size):
        if iir_filter_size not in self._possible_iir_filter_sizes:
            s = f"Unexpected iir_filter_size {iir_filter_size}."
            s += f" Choose one of {self._possible_iir_filter_sizes}."
            raise ValueError(s)
        self._iir_filter_size = iir_filter_size
        self.bme680.set_filter(self._possible_iir_filter_sizes.index(iir_filter_size))

    @property
    def temperature_offset(self):
        return self._temperature_offset

    @temperature_offset.setter
    def temperature_offset(self, temperature_offset):
        self._temperature_offset = temperature_offset
        self.bme680.set_temp_offset(temperature_offset)

    def get_sensor_data(self):
        self.bme680.get_sensor_data()
        return self.bme680.data
    