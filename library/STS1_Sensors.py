from smbus2 import i2c_msg
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


# ------------------------sensor wrapper class-----------------------------
class Sensors():
    BME688stat = True
    TMP112stat = True
    ADXL345stat = True
    BMM150stat = True
    GUVA_C32stat = True
    
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
            self.GUVA.set_address(0x39)
            self.GUVA.set_resolution(100)
            self.GUVA.set_range(128)
            self.GUVA.setup()
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
    
    
    
            


# ------------------------TMP112-----------------------------

class TMP112:
    poss_addr = [0x48, 0x49, 0x4A, 0x4B]
    poss_conversionrate = [0.25, 1, 4, 8]
    poss_conversionrate_bin = [0b00, 0b01, 0b10, 0b11]
        
    config_set = 0
    addr = 0
    mode = 0b1   #1 ... extended mode (13-Bit -55°C - 150°C) 0 ... normal mode (12-Bit -55°C - 128°C)
    conversionrate = 0
    
    setConversionrate = False
    setAddr = False
    setupD = False
    consoleLog = True
    def __init__(self, bus):
        self.addr = 0x48
        self.bus = bus
    def deact_consoleLog(self):
        self.consoleLog = False
    def set_mode(self, mode):
        if mode == 1:
            self.mode = 0b1
        elif mode == 0:
            self.mode = 0b0
        elif self.consoleLog:
            print("The mode entered is invalid. Please use 0 or 1 as the mode")
    def set_address(self, address):
        try:
            self.poss_addr.index(address)
            self.addr = address
            self.setAddr = True
        except ValueError:
            s = "The address (" + str(hex(address)) + ") you entered for the sensor TMP112 does not exist!"
            if self.consoleLog:
                print(s)
            s = "Try one of the following:"
            for value in self.poss_addr:
                s = s + str(hex(value)) + " "
            if self.consoleLog:
                print(s)
                print("TMP112 not initialized!!!")
    def set_conversionrate(self, rate):
        try:
            self.poss_conversionrate.index(rate)
            self.conversionrate = rate
            self.setConversionrate = True
        except ValueError:
            s = "The conversionrate (" + str(rate) + ") you entered for the sensor TMP112 does not exist!"
            if self.consoleLog:
                print(s)
            s = "Try one of the following:"
            for value in self.poss_conversionrate:
                s = s + str(value) + " "
            if self.consoleLog:
                print(s)
                print("TMP112 conversionrate not set!!!")
    def setup(self):
        if self.setAddr and self.setConversionrate:
            #all settings correct
            msg = i2c_msg.write(self.addr, [0b00000001,0b01100000,0b00100000 + ((self.poss_conversionrate_bin[self.poss_conversionrate.index(self.conversionrate)]) << 6)  + (self.mode << 4)])
            self.bus.i2c_rdwr(msg)
            self.setupD = True
            if self.consoleLog:
                print("Setup finished, TMP112 ready.")
        else:
            if self.consoleLog:
                print("Setup failed! Settings incorrect")
    def getTemp(self):
        if self.setupD:
            msg_w = i2c_msg.write(self.addr, [0b00000000])
            msg_r = i2c_msg.read(self.addr, 2)
            self.bus.i2c_rdwr(msg_w)
            self.bus.i2c_rdwr(msg_r)
            
            byte = []
            for value in msg_r:
                byte.append(value)
           
            raw = ((byte[0] << 8) + byte[1])>>(4-(self.mode))
            #print(bin(raw))
            #print(bin(raw>>(11+self.mode)))
            if (raw>>(11+self.mode)) == 0b1:
                #negative temp
                raw =  raw - (1<<(12+self.mode))
                #raw = (1<<(12-self.mode)) - raw
                #print("negativ")
            temp = raw * 0.0625
            
            return temp            
        else:
            if self.consoleLog:
                print("Setup not finished")
                
# ------------------------BME688-----------------------------


class bmeData:
    temperature = 0
    humidity = 0
    pressure = 0
    gasResistance = 0
    AQI = 0
    def __init__(self):
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0
        self.gasResistance = 0
    def setTemp(self, temp):
        self.temperature = temp
    def setHum(self, hum):
        self.humidity = hum
    def setPress(self, press):
        self.pressure = press
    def setGasRes(self, gasRes):
        self.gasResistance = gasRes
    def setAQI(self, AQI):
        self.AQI = AQI
    


class BME688:
    poss_addr = [0x76, 0x77]
    poss_tempOSR = [1, 2, 4, 8, 16]
    poss_tempOSR_bin = [0b001, 0b010, 0b011, 0b100, 0b101] #0x74 7/6/5
    poss_humOSR = [1, 2, 4, 8, 16]
    poss_humOSR_bin = [0b001, 0b010, 0b011, 0b100, 0b101] #0x72 2/1/0
    poss_pressOSR = [1, 2, 4, 8, 16]
    poss_pressOSR_bin = [0b001, 0b010, 0b011, 0b100, 0b101] #0x74 4/3/2
    poss_IIR = [0, 1, 3, 7, 15, 31, 63, 127]
    poss_IIR_bin = [0b000, 0b001, 0b010, 0b011, 0b100, 0b101, 0b110, 0b111]
    
    #poss_conversionrate = [0.25, 1, 4, 8]
    #poss_conversionrate_bin = [0b00, 0b01, 0b10, 0b11]
    

    config_set = 0
    addr = 0
    
    #mode = 0b1   #1 ... extended mode (13-Bit -55°C - 150°C) 0 ... normal mode (12-Bit -55°C - 128°C)
    #conversionrate = 0
    tempOSR = 0
    humOSR = 0
    pressOSR = 0
    tempRES = 0
    gasTemp = 0
    gasTime = 0
    IIR = 0
    #setConversionrate = False
    #setAddr = False
    setTempOSR = 0
    setHumOSR = 0
    setPressOSR = 0
    setGasTemp = 0
    setGas = 0
    setGasTime = 0
    setIIR = 0
    setupD = False
    consoleLog = True
    
    ambientTemp = 25
    
    par_t1 = 0
    par_t2 = 0
    par_t3 = 0
    par_h1 = 0
    par_h2 = 0
    par_h3 = 0
    par_h4 = 0
    par_h5 = 0
    par_h6 = 0
    par_h7 = 0
    par_p1 = 0
    par_p2 = 0
    par_p3 = 0
    par_p4 = 0
    par_p5 = 0
    par_p6 = 0
    par_p7 = 0
    par_p8 = 0
    par_p9 = 0
    par_p10 = 0
    par_g1 = 0
    par_g2 = 0
    par_g3 = 0
    
    def __init__(self, bus):
        self.addr = 0x76
        self.bus = bus
        self.output = bmeData()
    def deact_consoleLog(self):
        self.consoleLog = False
    def set_address(self, address):
        try:
            self.poss_addr.index(address)
            self.addr = address
            self.setAddr = True
        except ValueError:
            s = "The address (" + str(hex(address)) + ") you entered for the sensor BME688 does not exist!"
            if self.consoleLog:
                print(s)
            s = "Try one of the following:"
            for value in self.poss_addr:
                s = s + str(hex(value)) + " "
            if self.consoleLog:
                print(s)
                print("BME688 not initialized!!!")
    def set_tempOSR(self, OSR): #temperateure Oversamplingrate
        try:
            self.poss_tempOSR.index(OSR)
            self.tempOSR = OSR
            self.setTempOSR = True 
        except ValueError:
            s = "The temperature oversamplingrate (" + str(OSR) + ") you entered for the sensor BME688 does not exist!"
            if self.consoleLog:
                print(s)
            s = "Try one of the following:"
            for value in self.poss_tempOSR:
                s = s + str(value) + " "
            if self.consoleLog:
                print(s)
                print("BME688 temperature oversamplingrate not set!!!")
    def set_humOSR(self, OSR): #humidity Oversamplingrate
        try:
            self.poss_humOSR.index(OSR)
            self.humOSR = OSR
            self.setHumOSR = True 
        except ValueError:
            s = "The humidity oversamplingrate (" + str(OSR) + ") you entered for the sensor BME688 does not exist!"
            if self.consoleLog:
                print(s)
            s = "Try one of the following:"
            for value in self.poss_humOSR:
                s = s + str(value) + " "
            if self.consoleLog:
                print(s)
                print("BME688 humidity oversamplingrate not set!!!")
    def set_pressOSR(self, OSR): #pressure Oversamplingrate
        try:
            self.poss_pressOSR.index(OSR)
            self.pressOSR = OSR
            self.setPressOSR = True 
        except ValueError:
            s = "The pressure oversamplingrate (" + str(OSR) + ") you entered for the sensor BME688 does not exist!"
            if self.consoleLog:
                print(s)
            s = "Try one of the following:"
            for value in self.poss_pressOSR:
                s = s + str(value) + " "
            if self.consoleLog:
                print(s)
                print("BME688 pressure oversamplingrate not set!!!")
    def set_IIR(self, IIR):
        try:
            self.poss_IIR.index(IIR)
            self.IIR = IIR
            self.setIIR = True 
        except ValueError:
            s = "The IIR value (" + str(IIR) + ") you entered for the sensor BME688 does not exist!"
            if self.consoleLog:
                print(s)
            s = "Try one of the following:"
            for value in self.poss_IIR:
                s = s + str(value) + " "
            if self.consoleLog:
                print(s)
                print("BME688 temperature oversamplingrate not set!!!")
    def set_gasTemp(self, temp):
        if temp >= 200 and temp <= 400:
            self.gasTemp = temp
            self.setGasTemp = True
        else:
            s = "The temperature value (" + str(temp) + ") you entered for the sensor BME688 is outside of the possible range!"
            print(s)
            s = "Try a value between 200-400°C"
            print(s)
            print("BME688 temperature oversamplingrate not set!!!")
    def set_gasTime(self, time):
        if time > 0 and time < 4096:
            self.gasTime = time
            self.setGasTime = True
        else:
            s = "The time (" + str(temp) + ") you entered for the sensor BME688 is outside of the possible range!"
            print(s)
            s = "Try a value between 1-4096ms"
            print(s)
            print("BME688 temperature oversamplingrate not set!!!")
    def setup(self):
        if self.setAddr and self.setTempOSR and self.setIIR and self.setHumOSR and self.setPressOSR:
            
            if self.setGasTemp and self.setGasTime:
                #Enable GasTemp
                #print("setGas")
                self.bus.write_byte_data(self.addr, 0x72, 0b00000000 + (self.poss_humOSR_bin[self.poss_humOSR.index(self.humOSR)] << 0)) #set humidity oversamplingrate
                self.bus.write_byte_data(self.addr, 0x74, 0b00000000 + (self.poss_tempOSR_bin[self.poss_tempOSR.index(self.tempOSR)] << 5) + (self.poss_pressOSR_bin[self.poss_pressOSR.index(self.pressOSR)] << 2)) #set temperature oversamplingrate
                self.bus.write_byte_data(self.addr, 0x75, 0b00000000 + (self.poss_IIR_bin[self.poss_IIR.index(self.IIR)] << 2))
                
                self.bus.write_byte_data(self.addr, 0x71, 0b00100000) #enable gas conversion and activate heater step 0
                if self.gasTime / 1 <= 64:
                    gasTimeSet = 0b00000000 + int(self.gasTime)
                elif self.gasTime / 4 <= 64:
                    gasTimeSet = 0b01000000 + int(self.gasTime/4)
                elif self.gasTime / 16 <= 64:
                    gasTimeSet = 0b10000000 + int(self.gasTime/16)
                elif self.gasTime / 64 <= 64:
                    gasTimeSet = 0b11000000 + int(self.gasTime/64)
                #print("gasTimeSet: {0:08b}".format(gasTimeSet))
                self.bus.write_byte_data(self.addr, 0x64, gasTimeSet)                
                self.setGas = 1
            else:
                #only Temperature, Humidity and Pressure
                
                self.bus.write_byte_data(self.addr, 0x72, 0b00000000 + (self.poss_humOSR_bin[self.poss_humOSR.index(self.humOSR)] << 0)) #set humidity oversamplingrate
                self.bus.write_byte_data(self.addr, 0x74, 0b00000000 + (self.poss_tempOSR_bin[self.poss_tempOSR.index(self.tempOSR)] << 5) + (self.poss_pressOSR_bin[self.poss_pressOSR.index(self.pressOSR)] << 2)) #set temperature oversamplingrate
                self.bus.write_byte_data(self.addr, 0x75, 0b00000000 + (self.poss_IIR_bin[self.poss_IIR.index(self.IIR)] << 2))
                self.bus.write_byte_data(self.addr, 0x71, 0b00000000) 
                self.bus.write_byte_data(self.addr, 0x64, 0b00000000) 
                self.bus.write_byte_data(self.addr, 0x5A, 0b00000000)
                self.bus.write_byte_data(self.addr, 0x70, 0b00001000)
                
            #all settings correct
            
            
            self.setupD = True
            
            #get comp values
            par_t1_LSB = self.bus.read_byte_data(self.addr, 0xE9)
            par_t1_MSB = self.bus.read_byte_data(self.addr, 0xEA)
            self.par_t1 = twos_comp((par_t1_MSB<<8) + par_t1_LSB, 16)
                    
            par_t2_LSB = self.bus.read_byte_data(self.addr, 0x8A)
            par_t2_MSB = self.bus.read_byte_data(self.addr, 0x8B)
            self.par_t2 = twos_comp((par_t2_MSB<<8) + par_t2_LSB, 16)
            
            self.par_t3 = twos_comp(self.bus.read_byte_data(self.addr, 0x8C),8)
            
            par_h1_LSB = self.bus.read_byte_data(self.addr, 0xE2)
            par_h1_MSB = self.bus.read_byte_data(self.addr, 0xE3)
            self.par_h1 = twos_comp((par_h1_MSB<<4) + (par_h1_LSB & 0b00001111) ,12)
            
            par_h2_LSB = self.bus.read_byte_data(self.addr, 0xE2)
            par_h2_MSB = self.bus.read_byte_data(self.addr, 0xE1)
            self.par_h2 = twos_comp((par_h2_MSB<<4) + ((par_h2_LSB & 0b11110000) >> 4), 12)
            
            self.par_h3 = twos_comp(self.bus.read_byte_data(self.addr, 0xE4),8)
            
            self.par_h4 = twos_comp(self.bus.read_byte_data(self.addr, 0xE5),8)
            
            self.par_h5 = twos_comp(self.bus.read_byte_data(self.addr, 0xE6),8)
            
            self.par_h6 = twos_comp(self.bus.read_byte_data(self.addr, 0xE7),8)
            
            self.par_h7 = twos_comp(self.bus.read_byte_data(self.addr, 0xE8),8)
            
            par_p1_LSB = self.bus.read_byte_data(self.addr, 0x8E)
            par_p1_MSB = self.bus.read_byte_data(self.addr, 0x8F)
            self.par_p1 = (par_p1_MSB<<8) + par_p1_LSB
            
            par_p2_LSB = self.bus.read_byte_data(self.addr, 0x90)
            par_p2_MSB = self.bus.read_byte_data(self.addr, 0x91)
            self.par_p2 = twos_comp((par_p2_MSB<<8) + par_p2_LSB,16)
            
            self.par_p3 = twos_comp(self.bus.read_byte_data(self.addr, 0x92),8)
            
            par_p4_LSB = self.bus.read_byte_data(self.addr, 0x94)
            par_p4_MSB = self.bus.read_byte_data(self.addr, 0x95)
            self.par_p4 = twos_comp((par_p4_MSB<<8) + par_p4_LSB,16)
            
            par_p5_LSB = self.bus.read_byte_data(self.addr, 0x96)
            par_p5_MSB = self.bus.read_byte_data(self.addr, 0x97)
            self.par_p5 = twos_comp((par_p5_MSB<<8) + par_p5_LSB,16)
            
            self.par_p6 = twos_comp(self.bus.read_byte_data(self.addr, 0x99),8)
            
            self.par_p7 = twos_comp(self.bus.read_byte_data(self.addr, 0x98),8)
            
            par_p8_LSB = self.bus.read_byte_data(self.addr, 0x9C)
            par_p8_MSB = self.bus.read_byte_data(self.addr, 0x9D)
            self.par_p8 = twos_comp((par_p8_MSB<<8) + par_p8_LSB,16)
            
            par_p9_LSB = self.bus.read_byte_data(self.addr, 0x9E)
            par_p9_MSB = self.bus.read_byte_data(self.addr, 0x9F)
            self.par_p9 = twos_comp((par_p9_MSB<<8) + par_p9_LSB,16)
            
            self.par_p10 = twos_comp(self.bus.read_byte_data(self.addr, 0xA0),8)
            
            self.par_g1 = twos_comp(self.bus.read_byte_data(self.addr, 0xED),8)
            
            par_g2_LSB = self.bus.read_byte_data(self.addr, 0xEB)
            par_g2_MSB = self.bus.read_byte_data(self.addr, 0xEC)
            self.par_g2 = twos_comp((par_g2_MSB<<8) + par_g2_LSB,16)
            
            self.par_g3 = twos_comp(self.bus.read_byte_data(self.addr, 0xEE),8)
            
            self.res_heat_range = (self.bus.read_byte_data(self.addr, 0x02) & 0b00110000) >> 4
            
            self.res_heat_val = self.bus.read_byte_data(self.addr, 0x00)
            
            
            if self.setGas == True:
                varg1 = (self.par_g1 / 16.0) + 49.0
                varg2 = ((self.par_g2 / 32768.0) * 0.0005) + 0.00235
                varg3 = self.par_g3 / 1024.0
                varg4 = varg1 * (1.0 + (varg2 * self.gasTemp))
                varg5 = varg4 + (varg3 * self.ambientTemp)
                tempset = (3.4 * ((varg5 * (4.0 / (4.0 + self.res_heat_range)) * (1.0 / (1.0 + (self.res_heat_val * 0.002)))) - 25))
                #print("tempset: {0:08b}".format(int(tempset)))
                self.bus.write_byte_data(self.addr, 0x5A, int(tempset))
            
            #s = "t1:{0}\nt2:{1}\nt3:{2}\np1:{3}\np2:{4}\np3:{5}\np4:{6}\np5:{7}\np6:{8}\np7:{9}\np8:{10}\np9:{11}\np10:{12}\nh1:{13}\nh2:{14}\nh3:{15}\nh4:{16}\nh5:{17}\nh6:{18}\nh7:{19}\ng1:{20}\ng2:{21}\ng3:{22}\n"
            #print(s.format(self.par_t1, self.par_t2, self.par_t3, self.par_p1, self.par_p2, self.par_p3, self.par_p4, self.par_p5, self.par_p6, self.par_p7, self.par_p8, self.par_p9, self.par_p10, self.par_h1, self.par_h2, self.par_h3, self.par_h4, self.par_h5, self.par_h6, self.par_h7, self.par_g1, self.par_g2, self.par_g3))
            if self.consoleLog:
                #check things and eveluate the resolution of the temperature sensor
                if self.IIR != 0:
                    self.tempRES = 20 #20bit
                else:
                    self.tempRES = 16 + (self.poss_tempOSR_bin[self.poss_tempOSR.index(self.tempOSR)] - 1) 
                print("Setup finished, BME688 ready.")
        else:
            if self.consoleLog:
                print("Setup failed! Settings incorrect")
    def getVal(self):
        if self.setupD:
            #initiate force mode -> single measurement
            self.bus.write_byte_data(self.addr, 0x70, 0b00000000)
            self.bus.write_byte_data(self.addr, 0x74, 0b00000001 + (self.poss_tempOSR_bin[self.poss_tempOSR.index(self.tempOSR)] << 5) + (self.poss_pressOSR_bin[self.poss_pressOSR.index(self.pressOSR)] << 2))
            
            #if Gas measurement mode is active wait until gas measurement is finished
            gasReady = False
            if self.setGas == True:
                for i in range(10):
                    if self.bus.read_byte_data(self.addr, 0x1D) != 0b10000000:
                        time.sleep(0.05)
                        continue
                    gasReady = True
            """     
            while self.bus.read_byte_data(self.addr, 0x1D) != 0b10000000:
            #time.sleep(0.5)
            i = 0
            #do something
            """
            #get temperature adc value       
            temp_adc_MSB = self.bus.read_byte_data(self.addr, 0x22)
            temp_adc_LSB=  self.bus.read_byte_data(self.addr, 0x23)
            temp_adc_XSB = self.bus.read_byte_data(self.addr, 0x24)
            temp_adc = ((temp_adc_XSB & 0b11110000) >> 4) + (temp_adc_LSB << 4) + (temp_adc_MSB << 12)
            
            #compensate temperature adc value
            vart1 = ((temp_adc / 16384.0) - (self.par_t1 / 1024.0)) * self.par_t2
            vart2 = (((temp_adc / 131072.0) - (self.par_t1 / 8192.0)) * ((temp_adc / 131072.0) - (self.par_t1 / 8192.0))) * self.par_t3 * 16.0
            t_fine = vart1 + vart2
            temp_comp = t_fine / 5120.0
            
            self.ambientTemp = temp_comp
            
            
            #get humidity adc value
            hum_adc_MSB = self.bus.read_byte_data(self.addr, 0x25)
            hum_adc_LSB=  self.bus.read_byte_data(self.addr, 0x26)            
            hum_adc = (hum_adc_LSB << 0) + (hum_adc_MSB << 8)
            
            #compensate humidity adc value
            varh1 = hum_adc - ((self.par_h1 * 16.0) + ((self.par_h3 / 2.0) * temp_comp))
            varh2 = varh1 * ((self.par_h2 / 262144.0) * (1.0 + ((self.par_h4 / 16384.0) * temp_comp) + ((self.par_h5 / 1048576.0) * temp_comp * temp_comp)))
            varh3 = self.par_h6 / 16384.0
            varh4 = self.par_h7 / 2097152.0
            hum_comp = varh2 + ((varh3 + (varh4 * temp_comp)) * varh2 *varh2)
            
            #get pressure adc value 
            press_adc_MSB = self.bus.read_byte_data(self.addr, 0x1F)
            press_adc_LSB=  self.bus.read_byte_data(self.addr, 0x20)
            press_adc_XSB = self.bus.read_byte_data(self.addr, 0x21)
            press_adc = ((press_adc_XSB & 0b11110000) >> 4) + (press_adc_LSB << 4) + (press_adc_MSB << 12)
            
            #compensate pressure adc value
            varp1 = (t_fine / 2.0) - 64000.0
            varp2 = varp1 * varp1 * (self.par_p6 / 131072.0)
            varp2 = varp2 + (varp1 * (self.par_p5 * 2.0))
            varp2 = (varp2 / 4.0) + (self.par_p4 * 65536.0)
            varp1 = (((self.par_p3 * varp1 * varp1) / 16384.0) + (self.par_p2 * varp1)) / 524288.0
            varp1 = (1.0 + (varp1 / 32768.0)) * self.par_p1
            press_comp = 1048576.0 - press_adc
            press_comp = ((press_comp - (varp2 / 4096.0)) * 6250.0) / varp1
            varp1 = (self.par_p9 * press_comp * press_comp) / 2147483648.0
            varp2 = press_comp * (self.par_p8 / 32768.0)
            varp3 = (press_comp / 256.0) * (press_comp / 256.0) * (press_comp / 256.0) * (self.par_p10 / 131072.0)
            press_comp = press_comp + (varp1 + varp2 +  varp3 + (self.par_p7 * 128.0)) / 16.0
            
            #read gasresistence if enabled
            gas_res = 0
            if self.setGas == True and gasReady == True:
                gas_adc_MSB = self.bus.read_byte_data(self.addr, 0x2C)
                gas_adc_LSB=  self.bus.read_byte_data(self.addr, 0x2D)
                gas_adc = ((gas_adc_LSB & 0b11000000) >> 6) + (press_adc_MSB << 2)
                
                gas_range_XSB = self.bus.read_byte_data(self.addr, 0x2D)
                gas_range = gas_range_XSB & 0b00001111
                
                
                varg1 = 262144 >> gas_range
                varg2 = gas_adc - 512
                varg2 *= 3
                varg2 = 4096 + varg2
                gas_res = (10000.0 * varg1) / varg2
                gas_res *= 100.0
            
            #write values into object
            self.output.setHum(hum_comp)
            self.output.setTemp(temp_comp)
            self.output.setPress(press_comp)
            self.output.setGasRes(gas_res)
            
            #recalculate and set temperature
            
            if self.setGas == True:
                varg1 = (self.par_g1 / 16.0) + 49.0
                varg2 = ((self.par_g2 / 32768.0) * 0.0005) + 0.00235
                varg3 = self.par_g3 / 1024.0
                varg4 = varg1 * (1.0 + (varg2 * self.gasTemp))
                varg5 = varg4 + (varg3 * self.ambientTemp)
                tempset = (3.4 * ((varg5 * (4.0 / (4.0 + self.res_heat_range)) * (1.0 / (1.0 + (self.res_heat_val * 0.002)))) - 25))
                self.bus.write_byte_data(self.addr, 0x5A, int(tempset))

            #turn off heater
            self.bus.write_byte_data(self.addr, 0x70, 0b00001000)
            
            #return data object
            return self.output                 
        else:
            if self.consoleLog:
                print("Setup not finished")
                
# ------------------------GUVA_C32-----------------------------

class GUVA_C32:
    poss_addr = [0x39]
    poss_res = [100, 200, 400, 800]
    poss_res_bin = [0b011, 0b010, 0b001, 0b000]
    poss_range = [1, 2, 4, 8, 16, 32, 64, 128]
    poss_range_bin = [0b000, 0b001, 0b010, 0b011, 0b100, 0b101, 0b110, 0b111]
    
            
    addr = 0
    res = 0
    range_ = 0
    
       
    
    setAddr = False
    setRes = False
    setRange = False
    setupD = False
    consoleLog = True
    def __init__(self, bus):
        self.addr = 0x37
        self.bus = bus
    def deact_consoleLog(self):
        self.consoleLog = False
    def set_address(self, address):
        try:
            self.poss_addr.index(address)
            self.addr = address
            self.setAddr = True
        except ValueError:
            s = "The address (" + str(hex(address)) + ") you entered for the sensor GUVA_C32 does not exist!"
            if self.consoleLog:
                print(s)
            s = "Try one of the following:"
            for value in self.poss_addr:
                s = s + str(hex(value)) + " "
            if self.consoleLog:
                print(s)
                print("GUVA_C32 not initialized!!!")
    def set_resolution(self, res):
        try:
            self.poss_res.index(res)
            self.res = res
            self.setRes = True
        except ValueError:
            s = "The resolution (" + str(hex(address)) + ") you entered for the sensor GUVA_C32 does not exist!"
            if self.consoleLog:
                print(s)
            s = "Try one of the following:"
            for value in self.poss_res:
                s = s + str(hex(value)) + " "
            if self.consoleLog:
                print(s)
                print("GUVA_C32 not initialized!!!")
    def set_range(self, range_):
        try:
            self.poss_range.index(range_)
            self.range_ = range_
            self.setRange = True
        except ValueError:
            s = "The range (" + str(hex(address)) + ") you entered for the sensor GUVA_C32 does not exist!"
            if self.consoleLog:
                print(s)
            s = "Try one of the following:"
            for value in self.poss_range:
                s = s + str(hex(value)) + " "
            if self.consoleLog:
                print(s)
                print("GUVA_C32 not initialized!!!")
    def setup(self):
        if self.setAddr and self.setRes and self.setRange:
            #all settings correct
            #set power mode normal 0b00 and operation mode UVAoperation 0b01 -> 0b00010000 0x01
            msg = i2c_msg.write(self.addr, [0x01, 0b00010000])
            self.bus.i2c_rdwr(msg)
            #set resolution 0x04
            msg = i2c_msg.write(self.addr, [0x04, 0b00000011])
            #msg = i2c_msg.write(self.addr, [0x04, 0b00000000 + self.poss_res_bin[self.poss_res.index(self.res)]])
            self.bus.i2c_rdwr(msg)
            #set range  0x05
            msg = i2c_msg.write(self.addr, [0x05, 0b00000000])
            #msg = i2c_msg.write(self.addr, [0x05, 0b00000000 + self.poss_range_bin[self.poss_range.index(self.range_)]])
            self.bus.i2c_rdwr(msg)
            
            
            self.setupD = True
            if self.consoleLog:
                print("Setup finished, GUVA_C32 ready.")
        else:
            if self.consoleLog:
                print("Setup failed! Settings incorrect")
    def getRawUVA(self):
        if self.setupD:
            
            msg_w = i2c_msg.write(self.addr, [0x15])
            msg_r = i2c_msg.read(self.addr, 2)
            self.bus.i2c_rdwr(msg_w)
            self.bus.i2c_rdwr(msg_r)
            
            byte = []
            for value in msg_r:
                byte.append(value)
                #print(bin(value))
            
            raw = (byte[0] + (byte[1] << 8))
            
            return raw            
        else:
            if self.consoleLog:
                print("Setup not finished")
    def getUVA(self):
        if self.setupD:
            
            msg_w = i2c_msg.write(self.addr, [0x15])
            msg_r = i2c_msg.read(self.addr, 2)
            self.bus.i2c_rdwr(msg_w)
            self.bus.i2c_rdwr(msg_r)
            
            byte = []
            for value in msg_r:
                byte.append(value)
                #print(bin(value))
            
            raw = (byte[0] + (byte[1] << 8))
            
            return int(raw / (65536 / 16))          
        else:
            if self.consoleLog:
                print("Setup not finished")
                
# ------------------------ADXL345-----------------------------

class ADXL345:
    poss_addr = [0x1D, 0x3A, 0x3B, 0x53]
    poss_datarate = [0.10,0.2,0.39,0.78,1.56,3.13,6.25,12.5,25,50,100,200,400,800,1600,3200]
    poss_datarate_bin= [0b0000,0b0001,0b0010,0b0011,0b0100,0b0101,0b0110,0b0111,0b1000,0b1001,0b1010,0b1011,0b1100,0b1101,0b1110,0b1111]
    poss_range = [2,4,8,16]
    poss_range_bin = [0b00, 0b01, 0b10, 0b11]
    range_resolution = [0b1111111111,0b1111111111,0b1111111111,0b1111111111]
    
    config_set = 0
    addr = 0
    datarate = 0
    range = 0
    resolution = 0
    check = 0
    setRange = False
    setDatarate = False
    setAddr = False
    setupD = False
    consoleLog = True
    def __init__(self, bus):
        self.addr = 0x53
        self.bus = bus
    def deact_consoleLog(self):
        self.consoleLog = False
    def set_address(self, address):
        try:
            self.poss_addr.index(address)
            self.addr = address
            self.setAddr = True
        except ValueError:
            s = "The address (" + str(hex(address)) + ") you entered for the sensor ADXL345 does not exist!"
            if self.consoleLog:
                print(s)
            s = "Try one of the following:"
            for value in self.poss_addr:
                s = s + str(hex(value)) + " "
            if self.consoleLog:
                print(s)
                print("ADXL345 not initialized!!!")
    def set_datarate(self, rate):
        try:
            self.poss_datarate.index(rate)
            self.datarate = rate
            self.setDatarate = True
        except ValueError:
            s = "The datarate (" + str(rate) + ") you entered for the sensor ADXL345 does not exist!"
            if self.consoleLog:
                print(s)
            s = "Try one of the following:"
            for value in self.poss_datarate:
                s = s + str(value) + " "
            if self.consoleLog:
                print(s)
                print("ADXL345 datarate not set!!!")
    def set_range(self, range):
        try:
            self.poss_range.index(range)
            self.range = range
            self.resolution = self.range_resolution[self.poss_range.index(range)]
            self.setRange = True
        except ValueError:
            s = "The range (" + str(range) + ") you entered for the sensor ADXL345 does not exist!"
            if self.consoleLog:
                print(s)
            s = "Try one of the following:"
            for value in self.poss_range:
                s = s + str(value) + " "
            if self.consoleLog:
                print(s)
                print("ADXL345 range not set!!!")
    def setup(self):
        if self.setAddr and self.setDatarate and self.setRange:
            #all settings correct
            self.bus.write_byte_data(self.addr, 0x2C, self.poss_datarate_bin[self.poss_datarate.index(self.datarate)])
            self.bus.write_byte_data(self.addr, 0x2D, 0b00001000)
            self.bus.write_byte_data(self.addr, 0x31, 0b00001011 & self.poss_range_bin[self.poss_range.index(self.range)])
            self.setupD = True
            if self.consoleLog:
                print("Setup finished, ADXL345 ready.")
        else:
            if self.consoleLog:
                print("Setup failed! Settings incorrect")
    def getXRaw(self):
        if self.setupD:
            x_LSB = self.bus.read_byte_data(self.addr, 0x32)
            x_MSB= self.bus.read_byte_data(self.addr, 0x33)
            x = (x_MSB << 8) | (x_LSB << 0)
            if (x>>(16-1)) == 0b1:
                x = (1<<15) - (x & 0b0111111111111111)
                x = x * (-1)                
            return x
        else:
            if self.consoleLog:
                print("Setup not finished")
    def getYRaw(self):
        if self.setupD:
            y_LSB = self.bus.read_byte_data(self.addr, 0x34)
            y_MSB= self.bus.read_byte_data(self.addr, 0x35)
            y = (y_MSB << 8) | (y_LSB << 0)
            if (y>>(16-1)) == 0b1:
                y = (1<<15) - (y & 0b0111111111111111)
                y = y * (-1)
            return y
        else:
            if self.consoleLog:
                print("Setup not finished")
    def getZRaw(self):
        if self.setupD:
            z_LSB = self.bus.read_byte_data(self.addr, 0x36)
            z_MSB= self.bus.read_byte_data(self.addr, 0x37)
            z = (z_MSB << 8) | (z_LSB << 0)
            if (z>>(16-1)) == 0b1:
                z = (1<<15) - (z & 0b0111111111111111)
                z = z * (-1)
            return z            
        else:
            if self.consoleLog:
                print("Setup not finished")
    def getXGs(self):
        if self.setupD:
            xnew = self.bus.read_i2c_block_data(self.addr, 0x32, 2)
            x_MSB = xnew[1]
            x_LSB = xnew[0]
            #x_LSB = self.bus.read_byte_data(self.addr, 0x32)
            #x_MSB= self.bus.read_byte_data(self.addr, 0x33)
            x = (x_MSB << 8) | (x_LSB << 0)
            if (x>>(16-1)) == 0b1:
                x = (1<<15) - (x & 0b0111111111111111)
                x = x * (-1)
            #if (x & (1<<(16-1))):
                #x = x - (1<<16)
            x = (x / (self.resolution>>1)) * self.range
            return x
        else:
            if self.consoleLog:
                print("Setup not finished")
    def getYGs(self):
        if self.setupD:
            ynew = self.bus.read_i2c_block_data(self.addr, 0x34, 2)
            y_MSB = ynew[1]
            y_LSB = ynew[0]
            #y_LSB = self.bus.read_byte_data(self.addr, 0x34)
            #y_MSB= self.bus.read_byte_data(self.addr, 0x35)
            y = (y_MSB << 8) | (y_LSB << 0)
            if (y>>(16-1)) == 0b1:
                y = (1<<15) - (y & 0b0111111111111111)
                y = y * (-1)
            #if (y & (1<<(16-1))):
                #y = y - (1<<16)
            y = (y / (self.resolution>>1)) * self.range
            return y
        else:
            if self.consoleLog:
                print("Setup not finished")
    def getZGs(self):
        if self.setupD:
            znew = self.bus.read_i2c_block_data(self.addr, 0x36, 2)
            z_MSB = znew[1]
            z_LSB = znew[0]
            
            #z_LSB = self.bus.read_byte_data(self.addr, 0x36)
            #z_MSB= self.bus.read_byte_data(self.addr, 0x37)
            z = (z_MSB << 8) | (z_LSB << 0)
            
            if (z>>(16-1)) == 0b1:
                z = (1<<15) - (z & 0b0111111111111111)
                z = z * (-1)

            z = (z / (self.resolution>>1)) * self.range
            return z
        else:
            if self.consoleLog:
                print("Setup not finished")


# ------------------------BMM150-----------------------------

class BMM150:
    poss_addr = [0x10, 0x11, 0x12, 0x13]
    poss_datarate = [10,2,6,8,15,20,25,30]
    poss_datarate_bin= [0b000,0b001,0b010,0b011,0b100,0b101,0b110,0b111]
    
    config_set = 0
    addr = 0
    datarate = 0
    
    
    check = 0
    
    setDatarate = False
    setAddr = False
    setupD = False
    consoleLog = True
    def __init__(self, bus):
        self.addr = 0x10
        self.bus = bus
    def deact_consoleLog(self):
        self.consoleLog = False
    def set_address(self, address):
        try:
            self.poss_addr.index(address)
            self.addr = address
            self.setAddr = True
        except ValueError:
            s = "The address (" + str(hex(address)) + ") you entered for the sensor BMM150 does not exist!"
            if self.consoleLog:
                print(s)
            s = "Try one of the following:"
            for value in self.poss_addr:
                s = s + str(hex(value)) + " "
            if self.consoleLog:
                print(s)
                print("BMM150 not initialized!!!")
    def set_datarate(self, rate):
        try:
            self.poss_datarate.index(rate)
            self.datarate = rate
            self.setDatarate = True
        except ValueError:
            s = "The datarate (" + str(rate) + ") you entered for the sensor BMM150 does not exist!"
            if self.consoleLog:
                print(s)
            s = "Try one of the following:"
            for value in self.poss_datarate:
                s = s + str(value) + " "
            if self.consoleLog:
                print(s)
                print("BMM150 datarate not set!!!")
    def setup(self):
        if self.setAddr and self.setDatarate:
            #all settings correct
            self.bus.write_byte_data(self.addr, 0x4B, 0b00000001)
            self.bus.write_byte_data(self.addr, 0x4C, 0b00000000 & (self.poss_datarate_bin[self.poss_datarate.index(self.datarate)] << 3))
            self.bus.write_byte_data(self.addr, 0x51, 0b00001111)
            self.bus.write_byte_data(self.addr, 0x52, 0b00001111)
            self.setupD = True
            if self.consoleLog:
                print("Setup finished, BMM150 ready.")
        else:
            if self.consoleLog:
                print("Setup failed! Settings incorrect")
    def getXRaw(self):
        if self.setupD:
            x_LSB = self.bus.read_byte_data(self.addr, 0x42)
            x_MSB=  self.bus.read_byte_data(self.addr, 0x43)
            x_XSB = (x_MSB<<8) + x_LSB
            x_XSB = x_XSB >>3
            
            if (x_XSB>>(13-1)) == 0b1:
                X_XSB = (1<<12) - (x_XSB & 0b0111111111111)
                x_XSB = x_XSB * (-1)
                
                
            return x_XSB
        else:
            if self.consoleLog:
                print("Setup not finished")
    def getYRaw(self):
        if self.setupD:
            y_LSB = self.bus.read_byte_data(self.addr, 0x44)
            y_MSB=  self.bus.read_byte_data(self.addr, 0x45)
            y_XSB = (y_MSB<<8) + y_LSB
            y_XSB = y_XSB >>3
            
            if (y_XSB>>(13-1)) == 0b1:
                y_XSB = (1<<12) - (y_XSB & 0b0111111111111)
                y_XSB = y_XSB * (-1)
                
            return y_XSB
        else:
            if self.consoleLog:
                print("Setup not finished")
    def getZRaw(self):
        if self.setupD:
            z_LSB = self.bus.read_byte_data(self.addr, 0x42)
            z_MSB=  self.bus.read_byte_data(self.addr, 0x43)
            z_XSB = (z_MSB<<8) + z_LSB
            z_XSB = z_XSB >>3
            
            if (z_XSB>>(16-1)) == 0b1:
                z_XSB = (1<<15) - (z_XSB & 0b0111111111111111)
                z_XSB = z_XSB * (-1)
                
            return z_XSB           
        else:
            if self.consoleLog:
                print("Setup not finished")
    def getXuT(self):
        if self.setupD:
            x_LSB = self.bus.read_byte_data(self.addr, 0x42)
            x_MSB=  self.bus.read_byte_data(self.addr, 0x43)
            x_XSB = (x_MSB<<8) + x_LSB
            x_XSB = x_XSB >>3
            
            if (x_XSB>>(13-1)) == 0b1:
                #negative temp
                x_XSB =  x_XSB - (1<<(13))
                
            return x_XSB / 3.15076
        else:
            if self.consoleLog:
                print("Setup not finished")
    def getYuT(self):
        if self.setupD:
            y_LSB = self.bus.read_byte_data(self.addr, 0x44)
            y_MSB=  self.bus.read_byte_data(self.addr, 0x45)
            y_XSB = (y_MSB<<8) + y_LSB
            y_XSB = y_XSB >>3
            
            if (y_XSB>>(13-1)) == 0b1:
                #negative temp
                y_XSB =  y_XSB - (1<<(13))
                
            return y_XSB / 3.15076
        else:
            if self.consoleLog:
                print("Setup not finished")
    def getZuT(self):
        if self.setupD:
            z_LSB = self.bus.read_byte_data(self.addr, 0x46)
            z_MSB=  self.bus.read_byte_data(self.addr, 0x47)
            z_XSB = (z_MSB<<8) + z_LSB
            z_XSB = z_XSB >>1
            
            if (z_XSB>>(15-1)) == 0b1:
                #negative temp
                z_XSB =  z_XSB - (1<<(15))
                
            return z_XSB / 6.5536                 
        else:
            if self.consoleLog:
                print("Setup not finished")