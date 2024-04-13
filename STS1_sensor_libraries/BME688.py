def twos_comp(val, bits):
    if val & (1 << (bits - 1)) != 0:
        val = val - (1 << bits)
    return val

import time
import logging

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
    Error = False
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
            s = "BME688: The address (" + str(hex(address)) + ") you entered for the sensor BME688 does not exist!"
            if self.consoleLog:
                logging.error(s)
            s = "BME688: Try one of the following:"
            for value in self.poss_addr:
                s = s + str(hex(value)) + " "
            if self.consoleLog:
                logging.info(s)
                logging.error("BME688: not initialized!!!")
    def set_tempOSR(self, OSR): #temperateure Oversamplingrate
        try:
            self.poss_tempOSR.index(OSR)
            self.tempOSR = OSR
            self.setTempOSR = True 
        except ValueError:
            s = "BME688: The temperature oversamplingrate (" + str(OSR) + ") you entered for the sensor BME688 does not exist!"
            if self.consoleLog:
                logging.error(s)
            s = "BME688: Try one of the following:"
            for value in self.poss_tempOSR:
                s = s + str(value) + " "
            if self.consoleLog:
                logging.info(s)
                logging.error("BME688: temperature oversamplingrate not set!!!")
    def set_humOSR(self, OSR): #humidity Oversamplingrate
        try:
            self.poss_humOSR.index(OSR)
            self.humOSR = OSR
            self.setHumOSR = True 
        except ValueError:
            s = "BME688: The humidity oversamplingrate (" + str(OSR) + ") you entered for the sensor BME688 does not exist!"
            if self.consoleLog:
                logging.error(s)
            s = "BME688: Try one of the following:"
            for value in self.poss_humOSR:
                s = s + str(value) + " "
            if self.consoleLog:
                logging.info(s)
                logging.error("BME688: humidity oversamplingrate not set!!!")
    def set_pressOSR(self, OSR): #pressure Oversamplingrate
        try:
            self.poss_pressOSR.index(OSR)
            self.pressOSR = OSR
            self.setPressOSR = True 
        except ValueError:
            s = "BME688: The pressure oversamplingrate (" + str(OSR) + ") you entered for the sensor BME688 does not exist!"
            if self.consoleLog:
                logging.error(s)
            s = "BME688: Try one of the following:"
            for value in self.poss_pressOSR:
                s = s + str(value) + " "
            if self.consoleLog:
                logging.info(s)
                logging.error("BME688: pressure oversamplingrate not set!!!")
    def set_IIR(self, IIR):
        try:
            self.poss_IIR.index(IIR)
            self.IIR = IIR
            self.setIIR = True 
        except ValueError:
            s = "BME688: The IIR value (" + str(IIR) + ") you entered for the sensor BME688 does not exist!"
            if self.consoleLog:
                logging.error(s)
            s = "BME688: Try one of the following:"
            for value in self.poss_IIR:
                s = s + str(value) + " "
            if self.consoleLog:
                logging.info(s)
                logging.error("BME688: temperature oversamplingrate not set!!!")
    def set_gasTemp(self, temp):
        if temp >= 200 and temp <= 400:
            self.gasTemp = temp
            self.setGasTemp = True
        else:
            s = "BME688: The temperature value (" + str(temp) + ") you entered for the sensor BME688 is outside of the possible range!"
            logging.error(s)
            s = "BME688: Try a value between 200-400°C"
            logging.info(s)
            logging.error("BME688: temperature oversamplingrate not set!!!")
    def set_gasTime(self, time):
        if time > 0 and time < 4096:
            self.gasTime = time
            self.setGasTime = True
        else:
            s = "BME688: The time (" + str(temp) + ") you entered for the sensor BME688 is outside of the possible range!"
            logging.error(s)
            s = "BME688: Try a value between 1-4096ms"
            logging.info(s)
            logging.error("BME688: temperature oversamplingrate not set!!!")
    def setup(self):
        if self.setAddr and self.setTempOSR and self.setIIR and self.setHumOSR and self.setPressOSR:
            try:
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
            except OSError as e:
                self.Error = True
                if e.errno == 121:
                    #print("Remote I/O Error: The device is not responding on the bus. Therefore it will be ignored")
                    logging.error("BME688: Remote I/O Error: The device is not responding on the bus. Therefore it will be ignored")
                else:
                    #print(f"An error occurred: {e}")
                    logging.error(f"BME688: An error occurred: {e}")
                return None
                    
                
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
                logging.info("BME688: Setup finished, sensor ready.")
        else:
            if self.consoleLog:
                logging.error("BME688: Setup failed! Settings incorrect")
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
                if self.Error:
                    #print("GUVA_C32 not available")
                    logging.error("BME688: not available")
                else:
                    #print("Setup not finished")
                    logging.error("BME688: Setup not finished")