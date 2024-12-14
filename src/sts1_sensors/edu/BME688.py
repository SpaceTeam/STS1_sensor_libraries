import os
import time

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
                 temperature_offset=0, enable_gas_measurements=False,
                 gas_heater_temperature=320, gas_heater_duration=150,
                 address=None, bus=None):
        super().__init__(possible_addresses=[0x76, 0x77], bus=bus)

        self.address = address or int(os.environ.get("STS1_SENSOR_ADDRESS_BME688", "0x76"), 16)
        self.bme680 = bme680.BME680(self.address, self.bus)
        self.last_query_time_ms = round(time.time() * 1000)

        self.temperature_osr = temperature_osr
        self.humidity_osr = humidity_osr
        self.pressure_osr = pressure_osr
        self.temperature_offset = temperature_offset
        self.iir_filter_size = iir_filter_size

        self.enable_gas_measurements = enable_gas_measurements
        self.gas_heater_temperature = gas_heater_temperature
        self.gas_heater_duration = gas_heater_duration

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
    
    @property
    def enable_gas_measurements(self):
        return self._enable_gas_measurements

    @enable_gas_measurements.setter
    def enable_gas_measurements(self, enable_gas_measurements):
        self._enable_gas_measurements = enable_gas_measurements
        if enable_gas_measurements:
            self.bme680.set_gas_status(bme680.ENABLE_GAS_MEAS)
        else:
            self.bme680.set_gas_status(bme680.DISABLE_GAS_MEAS)

    @property
    def gas_heater_temperature(self):
        return self._gas_heater_temperature

    @gas_heater_temperature.setter
    def gas_heater_temperature(self, gas_heater_temperature):
        self._gas_heater_temperature = gas_heater_temperature
        self.bme680.set_gas_heater_temperature(gas_heater_temperature)

    @property
    def gas_heater_duration(self):
        return self._gas_heater_duration

    @gas_heater_duration.setter
    def gas_heater_duration(self, gas_heater_duration):
        self._gas_heater_duration = gas_heater_duration
        self.bme680.set_gas_heater_duration(gas_heater_duration)

    def get_all_data(self):
        curr_time_ms = round(time.time() * 1000)
        if curr_time_ms - self.last_query_time_ms >= 10:
            self.bme680.get_sensor_data()
            self.last_query_time_ms = curr_time_ms
        return self.bme680.data
    
    def get_heat_stable(self):
        return self.get_all_data().heat_stable
    
    def get_temperature(self):
        # Temperature in degree celsius
        return self.get_all_data().temperature

    def get_pressure(self):
        # Pressure in hPa
        return self.get_all_data().pressure
    
    def get_humidity(self):
        # Humidity in % relative humidity
        return self.get_all_data().humidity
    
    def get_gas_resistance(self):
        # Gas resistance in Ohms
        return self.get_all_data().gas_resistance
    