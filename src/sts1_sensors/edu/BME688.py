from collections import namedtuple
import os
import time

from sts1_sensors.utils.AbstractSensor import AbstractSensor
from sts1_sensors.utils.utils import twos_comp

BME688Data = namedtuple("BME688Data", "pressure_hPa humidity_percent temperature_C gas_resistance_ohms")

class BME688(AbstractSensor):
    """Pressure, humidity, temperature and gas sensor.
    """
    # over-sampling rates
    _possible_temperature_osrs = [1, 2, 4, 8, 16]
    _possible_humidity_osrs = [1, 2, 4, 8, 16]
    _possible_pressure_osrs = [1, 2, 4, 8, 16]
    
    # filter coefficients iir filter. applies to temperature and pressure data only.
    _possible_iirs = [0, 1, 3, 7, 15, 31, 63, 127]
    
    def __init__(self, temperature_osr=1, humidity_osr=1, pressure_osr=1, iir=1, 
                 use_gas=True, gas_temperature=200, gas_time=1000,
                 address=None, bus=None):
        super().__init__(possible_addresses=[0x76, 0x77], bus=bus)

        self.address = address or int(os.environ.get("STS1_SENSOR_ADDRESS_BME688", "0x76"), 16)
        self.temperature_osr = temperature_osr
        self.humidity_osr = humidity_osr
        self.pressure_osr = pressure_osr
        self.iir = iir
        self.use_gas = use_gas
        self.gas_temperature = gas_temperature
        self.gas_time = gas_time

        self.ambient_temp = 25
        self.par_t1 = 0
        self.par_t2 = 0
        self.par_t3 = 0
        self.par_h1 = 0
        self.par_h2 = 0
        self.par_h3 = 0
        self.par_h4 = 0
        self.par_h5 = 0
        self.par_h6 = 0
        self.par_h7 = 0
        self.par_p1 = 0
        self.par_p2 = 0
        self.par_p3 = 0
        self.par_p4 = 0
        self.par_p5 = 0
        self.par_p6 = 0
        self.par_p7 = 0
        self.par_p8 = 0
        self.par_p9 = 0
        self.par_p10 = 0
        self.par_g1 = 0
        self.par_g2 = 0
        self.par_g3 = 0

        self._finish_setup()

    @property
    def temperature_osr(self):
        return self._temperature_osr

    @temperature_osr.setter
    def temperature_osr(self, temperature_osr):
        if temperature_osr not in self._possible_temperature_osrs:
            s = f"The temperature_osr {temperature_osr} does not exist."
            s += f" Choose one of {self._possible_temperature_osrs}."
            raise ValueError(s)
        self._temperature_osr = temperature_osr

    @property
    def humidity_osr(self):
        return self._humidity_osr

    @humidity_osr.setter
    def humidity_osr(self, humidity_osr):
        if humidity_osr not in self._possible_humidity_osrs:
            s = f"The humidity_osr {humidity_osr} does not exist."
            s += f" Choose one of {self._possible_humidity_osrs}."
            raise ValueError(s)
        self._humidity_osr = humidity_osr

    @property
    def pressure_osr(self):
        return self._pressure_osr

    @pressure_osr.setter
    def pressure_osr(self, pressure_osr):
        if pressure_osr not in self._possible_pressure_osrs:
            s = f"The pressure_osr {pressure_osr} does not exist."
            s += f" Choose one of {self._possible_pressure_osrs}."
            raise ValueError(s)
        self._pressure_osr = pressure_osr     

    @property
    def iir(self):
        return self._iir

    @iir.setter
    def iir(self, iir):
        if iir not in self._possible_iirs:
            s = f"The iir {iir} does not exist."
            s += f" Choose one of {self._possible_iirs}."
            raise ValueError(s)
        self._iir = iir

    @property
    def gas_temperature(self):
        return self._gas_temperature

    @gas_temperature.setter
    def gas_temperature(self, gas_temperature):
        if gas_temperature < 200 or gas_temperature > 400:
            raise ValueError(f"gas_temperature has to be between 200° and 400° Celcius (both inclusive) but was {gas_temperature}.")
        self._gas_temperature = gas_temperature

    @property
    def gas_time(self):
        return self._gas_time

    @gas_time.setter
    def gas_time(self, gas_time):
        if gas_time <= 0 or gas_time >= 4096:
            raise ValueError(f"gas_time has to be between 0 and 4095 ms (both inclusive) but was {gas_time}.")
        self._gas_time = gas_time

    def _finish_setup(self):
        h = self._possible_humidity_osrs.index(self.humidity_osr)
        self.bus.write_byte_data(self.address, 0x72, h)

        t = self._possible_temperature_osrs.index(self.temperature_osr) << 5
        p = self._possible_pressure_osrs.index(self.pressure_osr) << 2
        self.bus.write_byte_data(self.address, 0x74, t + p)

        iir = self._possible_iirs.index(self.iir) << 2
        self.bus.write_byte_data(self.address, 0x75, iir)
        
        if self.use_gas:
            # enable gas conversion and activate heater step 0
            self.bus.write_byte_data(self.address, 0x71, 0b00100000) 
            if self.gas_time <= 64:
                t = self.gas_time
            elif self.gas_time / 4 <= 64:
                t = 0b01000000 + self.gas_time // 4
            elif self.gas_time / 16 <= 64:
                t = 0b10000000 + self.gas_time // 16
            elif self.gas_time / 64 <= 64:
                t = 0b11000000 + self.gas_time // 64

            self.bus.write_byte_data(self.address, 0x64, t)                
            
        else:
            # only Temperature, Humidity and Pressure
            self.bus.write_byte_data(self.address, 0x71, 0) 
            self.bus.write_byte_data(self.address, 0x64, 0) 
            self.bus.write_byte_data(self.address, 0x5A, 0)
            self.bus.write_byte_data(self.address, 0x70, 0b1000)
        
        #get comp values
        par_t1_LSB = self.bus.read_byte_data(self.address, 0xE9)
        par_t1_MSB = self.bus.read_byte_data(self.address, 0xEA)
        self.par_t1 = twos_comp((par_t1_MSB<<8) + par_t1_LSB, 16)
                
        par_t2_LSB = self.bus.read_byte_data(self.address, 0x8A)
        par_t2_MSB = self.bus.read_byte_data(self.address, 0x8B)
        self.par_t2 = twos_comp((par_t2_MSB<<8) + par_t2_LSB, 16)
        
        self.par_t3 = twos_comp(self.bus.read_byte_data(self.address, 0x8C),8)
        
        par_h1_LSB = self.bus.read_byte_data(self.address, 0xE2)
        par_h1_MSB = self.bus.read_byte_data(self.address, 0xE3)
        self.par_h1 = twos_comp((par_h1_MSB<<4) + (par_h1_LSB & 0b00001111), 12)
        
        par_h2_LSB = self.bus.read_byte_data(self.address, 0xE2)
        par_h2_MSB = self.bus.read_byte_data(self.address, 0xE1)
        self.par_h2 = twos_comp((par_h2_MSB<<4) + ((par_h2_LSB & 0b11110000) >> 4), 12)
        
        self.par_h3 = twos_comp(self.bus.read_byte_data(self.address, 0xE4),8)
        self.par_h4 = twos_comp(self.bus.read_byte_data(self.address, 0xE5),8)
        self.par_h5 = twos_comp(self.bus.read_byte_data(self.address, 0xE6),8)
        self.par_h6 = twos_comp(self.bus.read_byte_data(self.address, 0xE7),8)
        self.par_h7 = twos_comp(self.bus.read_byte_data(self.address, 0xE8),8)
        
        par_p1_LSB = self.bus.read_byte_data(self.address, 0x8E)
        par_p1_MSB = self.bus.read_byte_data(self.address, 0x8F)
        self.par_p1 = (par_p1_MSB<<8) + par_p1_LSB
        
        par_p2_LSB = self.bus.read_byte_data(self.address, 0x90)
        par_p2_MSB = self.bus.read_byte_data(self.address, 0x91)
        self.par_p2 = twos_comp((par_p2_MSB<<8) + par_p2_LSB,16)
        
        self.par_p3 = twos_comp(self.bus.read_byte_data(self.address, 0x92),8)
        
        par_p4_LSB = self.bus.read_byte_data(self.address, 0x94)
        par_p4_MSB = self.bus.read_byte_data(self.address, 0x95)
        self.par_p4 = twos_comp((par_p4_MSB<<8) + par_p4_LSB,16)
        
        par_p5_LSB = self.bus.read_byte_data(self.address, 0x96)
        par_p5_MSB = self.bus.read_byte_data(self.address, 0x97)
        self.par_p5 = twos_comp((par_p5_MSB<<8) + par_p5_LSB,16)
        
        self.par_p6 = twos_comp(self.bus.read_byte_data(self.address, 0x99),8)
        
        self.par_p7 = twos_comp(self.bus.read_byte_data(self.address, 0x98),8)
        
        par_p8_LSB = self.bus.read_byte_data(self.address, 0x9C)
        par_p8_MSB = self.bus.read_byte_data(self.address, 0x9D)
        self.par_p8 = twos_comp((par_p8_MSB<<8) + par_p8_LSB,16)
        
        par_p9_LSB = self.bus.read_byte_data(self.address, 0x9E)
        par_p9_MSB = self.bus.read_byte_data(self.address, 0x9F)
        self.par_p9 = twos_comp((par_p9_MSB<<8) + par_p9_LSB,16)
        
        self.par_p10 = twos_comp(self.bus.read_byte_data(self.address, 0xA0),8)
        
        self.par_g1 = twos_comp(self.bus.read_byte_data(self.address, 0xED),8)
        
        par_g2_LSB = self.bus.read_byte_data(self.address, 0xEB)
        par_g2_MSB = self.bus.read_byte_data(self.address, 0xEC)
        self.par_g2 = twos_comp((par_g2_MSB<<8) + par_g2_LSB,16)
        
        self.par_g3 = twos_comp(self.bus.read_byte_data(self.address, 0xEE),8)
        
        self.res_heat_range = (self.bus.read_byte_data(self.address, 0x02) & 0b00110000) >> 4
        
        self.res_heat_val = self.bus.read_byte_data(self.address, 0x00)
        
        if self.use_gas:
            varg1 = (self.par_g1 / 16) + 49
            varg2 = ((self.par_g2 / 32768) * 0.0005) + 0.00235
            varg3 = self.par_g3 / 1024
            varg4 = varg1 * (1 + (varg2 * self.gas_temperature))
            varg5 = varg4 + (varg3 * self.ambient_temp)
            tempset = (3.4 * ((varg5 * (4 / (4 + self.res_heat_range)) * (1 / (1 + (self.res_heat_val * 0.002)))) - 25))
            
            self.bus.write_byte_data(self.address, 0x5A, int(tempset))
        
    def get_values(self):
        # initiate force mode -> single measurement
        self.bus.write_byte_data(self.address, 0x70, 0)

        t = self._possible_temperature_osrs.index(self.temperature_osr) << 5
        p = self._possible_pressure_osrs.index(self.pressure_osr) << 2
        self.bus.write_byte_data(self.address, 0x74, 1 + t + p)
        
        # if gas measurement mode is active wait until gas measurement is finished
        gas_ready = False
        if self.use_gas:
            for _ in range(10):
                if self.bus.read_byte_data(self.address, 0x1D) == 0b10000000:
                    break    
                time.sleep(0.05)
                    
                gas_ready = True

        # get temperature adc value       
        temp_adc_MSB = self.bus.read_byte_data(self.address, 0x22)
        temp_adc_LSB = self.bus.read_byte_data(self.address, 0x23)
        temp_adc_XSB = self.bus.read_byte_data(self.address, 0x24)
        temp_adc = ((temp_adc_XSB & 0b11110000) >> 4) + (temp_adc_LSB << 4) + (temp_adc_MSB << 12)
        
        # compensate temperature adc value
        vart1 = ((temp_adc / 16384) - (self.par_t1 / 1024)) * self.par_t2
        vart2 = (((temp_adc / 131072) - (self.par_t1 / 8192)) * ((temp_adc / 131072) - (self.par_t1 / 8192))) * self.par_t3 * 16
        t_fine = vart1 + vart2
        temp_comp = t_fine / 5120
        
        self.ambient_temp = temp_comp
        
        
        #get humidity adc value
        hum_adc_MSB = self.bus.read_byte_data(self.address, 0x25)
        hum_adc_LSB = self.bus.read_byte_data(self.address, 0x26)            
        hum_adc = (hum_adc_LSB << 0) + (hum_adc_MSB << 8)
        
        #compensate humidity adc value
        varh1 = hum_adc - ((self.par_h1 * 16) + ((self.par_h3 / 2) * temp_comp))
        varh2 = varh1 * ((self.par_h2 / 262144) * (1 + ((self.par_h4 / 16384) * temp_comp) + ((self.par_h5 / 1048576) * temp_comp * temp_comp)))
        varh3 = self.par_h6 / 16384
        varh4 = self.par_h7 / 2097152
        hum_comp = varh2 + ((varh3 + (varh4 * temp_comp)) * varh2 * varh2)
        
        #get pressure adc value 
        press_adc_MSB = self.bus.read_byte_data(self.address, 0x1F)
        press_adc_LSB = self.bus.read_byte_data(self.address, 0x20)
        press_adc_XSB = self.bus.read_byte_data(self.address, 0x21)
        press_adc = ((press_adc_XSB & 0b11110000) >> 4) + (press_adc_LSB << 4) + (press_adc_MSB << 12)
        
        #compensate pressure adc value
        varp1 = (t_fine / 2) - 64000
        varp2 = varp1 * varp1 * (self.par_p6 / 131072)
        varp2 = varp2 + (varp1 * (self.par_p5 * 2))
        varp2 = (varp2 / 4) + (self.par_p4 * 65536)
        varp1 = (((self.par_p3 * varp1 * varp1) / 16384) + (self.par_p2 * varp1)) / 524288
        varp1 = (1 + (varp1 / 32768)) * self.par_p1
        press_comp = 1048576 - press_adc
        press_comp = ((press_comp - (varp2 / 4096)) * 6250) / varp1
        varp1 = (self.par_p9 * press_comp * press_comp) / 2147483648
        varp2 = press_comp * (self.par_p8 / 32768)
        varp3 = (press_comp / 256) * (press_comp / 256) * (press_comp / 256) * (self.par_p10 / 131072)
        press_comp = press_comp + (varp1 + varp2 + varp3 + (self.par_p7 * 128)) / 16
        
        #read gasresistence if enabled
        gas_res = 0
        if self.use_gas and gas_ready:
            gas_adc_MSB = self.bus.read_byte_data(self.address, 0x2C)
            gas_adc_LSB = self.bus.read_byte_data(self.address, 0x2D)
            gas_adc = ((gas_adc_LSB & 0b11000000) >> 6) + (gas_adc_MSB << 2)
            
            gas_range_XSB = self.bus.read_byte_data(self.address, 0x2D)
            gas_range = gas_range_XSB & 0b00001111
            
            varg1 = 262144 >> gas_range
            varg2 = gas_adc - 512
            varg2 *= 3
            varg2 = 4096 + varg2
            gas_res = (10000 * varg1) / varg2
            gas_res *= 100
        
        
        #recalculate and set temperature
        if self.use_gas:
            varg1 = (self.par_g1 / 16) + 49
            varg2 = ((self.par_g2 / 32768) * 0.0005) + 0.00235
            varg3 = self.par_g3 / 1024
            varg4 = varg1 * (1 + (varg2 * self.gas_temperature))
            varg5 = varg4 + (varg3 * self.ambient_temp)
            tempset = (3.4 * ((varg5 * (4 / (4 + self.res_heat_range)) * (1 / (1 + (self.res_heat_val * 0.002)))) - 25))
            self.bus.write_byte_data(self.address, 0x5A, int(tempset))

        #turn off heater
        self.bus.write_byte_data(self.address, 0x70, 0b1000)
        
        return BME688Data(press_comp, hum_comp, temp_comp, gas_res)
