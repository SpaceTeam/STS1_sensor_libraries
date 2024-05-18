import logging
import time

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
    Error = False
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
            s = "BMM150: The address (" + str(hex(address)) + ") you entered for the sensor BMM150 does not exist!"
            if self.consoleLog:
                logging.error(s)
            s = "BMM150: Try one of the following:"
            for value in self.poss_addr:
                s = s + str(hex(value)) + " "
            if self.consoleLog:
                logging.info(s)
                logging.error("BMM150: not initialized!!!")
    def set_datarate(self, rate):
        try:
            self.poss_datarate.index(rate)
            self.datarate = rate
            self.setDatarate = True
        except ValueError:
            s = "BMM150: The datarate (" + str(rate) + ") you entered for the sensor BMM150 does not exist!"
            if self.consoleLog:
                logging.error(s)
            s = "BMM150: Try one of the following:"
            for value in self.poss_datarate:
                s = s + str(value) + " "
            if self.consoleLog:
                logging.info(s)
                logging.error("BMM150: datarate not set!!!")
    def setup(self):
        if self.setAddr and self.setDatarate:
            #all settings correct
            try:
                self.bus.write_byte_data(self.addr, 0x4B, 0b00000001)
                time.sleep(1)
                self.bus.write_byte_data(self.addr, 0x4C, 0b00000000 & (self.poss_datarate_bin[self.poss_datarate.index(self.datarate)] << 3))
                self.bus.write_byte_data(self.addr, 0x51, 0b00001111)
                self.bus.write_byte_data(self.addr, 0x52, 0b00001111)
            except OSError as e:
                self.Error = True
                if e.errno == 121:
                    logging.error("BMM150: Remote I/O Error: The device is not responding on the bus. Therefore it will be ignored")
                else:
                    logging.error(f"BMM150: An error occurred: {e}")
                return None
                    
            self.setupD = True
            if self.consoleLog:
                logging.info("BMM150: Setup finished, sensor ready.")
        else:
            if self.consoleLog:
                logging.error("BMM150: Setup failed! Settings incorrect")
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
                if self.Error:
                    logging.error("BMM150: not available")
                else:
                    logging.error("BMM150: Setup not finished")
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
                if self.Error:
                    logging.error("BMM150: not available")
                else:
                    logging.error("BMM150: Setup not finished")
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
                if self.Error:
                    logging.error("BMM150: not available")
                else:
                    logging.error("BMM150: Setup not finished")
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
                if self.Error:
                    logging.error("BMM150: not available")
                else:
                    logging.error("BMM150: Setup not finished")
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
                if self.Error:
                    logging.error("BMM150: not available")
                else:
                    logging.error("BMM150: Setup not finished")
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
                if self.Error:
                    logging.error("BMM150: not available")
                else:
                    logging.error("BMM150: Setup not finished")
