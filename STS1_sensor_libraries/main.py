from smbus2 import i2c_msg
from .ADXL345 import ADXL345
from .TMP112 import TMP112
from .BMM150 import BMM150
from .L3GD20H import L3GD20H
from .GUVA_C32 import GUVA_C32
from .BME688 import BME688
import time

def twos_comp(val, bits):
    if val & (1 << (bits - 1)) != 0:
        val = val - (1 << bits)
    return val

def current_millis_time():
    return round(time.time()*1000)

# ------------------------sensor wrapper output data class-----------------------------
class SensorsData():
    tempTMP = 0
    tempBME = 0
    hum = 0
    press = 0
    gasRes = 0
    accX = 0
    accY = 0
    accZ = 0
    gX = 0
    gY = 0
    gZ = 0
    uva = 0
    uvaI = 0
    magX = 0
    magY = 0
    magZ = 0
    angVelX = 0
    angVelY = 0
    angVelZ = 0


# ------------------------sensor wrapper class-----------------------------
class Sensors():
    BME688stat = True
    TMP112stat = True
    ADXL345stat = True
    BMM150stat = True
    GUVA_C32stat = True
    L3GD20Hstat = True
    
    
    lastBME = 0
    
    bus = 0
    def __init__(self, bus):
        self.bus = bus
        self.output = SensorsData()
    def disable_BME688(self):
        self.BME688stat = False
    def disable_TMP112(self):
        self.TMP112stat = False
    def disable_ADXL345(self):
        self.ADXL345stat = False
    def disable_BMM150(self):
        self.BMM150stat = False
    def disable_GUVA_C32(self):
        self.GUVA_C32stat = False
    def disable_L3GD20H(self):
        self.L3GD20Hstat = False
    def setup(self):
        if self.BME688stat:
            self.BME = BME688(self.bus)
            self.BME.set_address(0x76)
            self.BME.set_tempOSR(2)
            self.BME.set_humOSR(4)
            self.BME.set_pressOSR(8)
            self.BME.set_IIR(3)
            self.BME.set_gasTemp(320)
            self.BME.set_gasTime(150)
            self.BME.setup()
        if self.TMP112stat:
            self.TMP = TMP112(self.bus)
            self.TMP.set_address(0x48)
            self.TMP.set_conversionrate(4)
            self.TMP.set_mode(1)
            self.TMP.setup()
        if self.ADXL345stat:
            self.ADXL = ADXL345(self.bus)
            self.ADXL.set_address(0x53)
            self.ADXL.set_datarate(100)
            self.ADXL.set_range(2)
            self.ADXL.setup()
        if self.BMM150stat:
            self.BMM = BMM150(self.bus)
            self.BMM.set_address(0x10)
            self.BMM.set_datarate(30)
            self.BMM.setup()
        if self.GUVA_C32stat:
            self.GUVA = GUVA_C32(self.bus)
            self.GUVA.set_address(0x00)
            self.GUVA.set_resolution(100)
            self.GUVA.set_range(128)
            self.GUVA.setup()
        if self.L3GD20Hstat:
            self.L3GD20H = L3GD20H(self.bus)
            self.L3GD20H.set_address(0x6A)
            self.L3GD20H.set_datarate(800)
            self.L3GD20H.set_range(2000)
            self.L3GD20H.setup()
            
    def getData(self):
        #TMP112
        if self.TMP112stat:
            self.output.tempTMP = self.TMP.getTemp()
        
        #BME688
        if self.BME688stat:
            if(current_millis_time() - self.lastBME > 1000):
                val = self.BME.getVal()
                self.output.tempBME = val.temperature
                self.output.hum = val.humidity
                self.output.press = val.pressure
                self.output.gasRes = val.gasResistance
                self.lastBME = current_millis_time()
        
        #BMM150
        if self.BMM150stat:
            self.output.magX = self.BMM.getXuT()
            self.output.magY = self.BMM.getYuT()
            self.output.magZ = self.BMM.getZuT()
        
        #ADXL345
        if self.ADXL345stat:
            self.output.accX = self.ADXL.getXRaw()
            self.output.accY = self.ADXL.getYRaw()
            self.output.accZ = self.ADXL.getZRaw()
            
            self.output.gX = self.ADXL.getXGs()
            self.output.gY = self.ADXL.getYGs()
            self.output.gZ = self.ADXL.getZGs()
        
        #GUVA_C32
        if self.GUVA_C32stat:
            self.output.uva = self.GUVA.getRawUVA()
            self.output.uvaI = self.GUVA.getUVA()
        
        return self.output


                

