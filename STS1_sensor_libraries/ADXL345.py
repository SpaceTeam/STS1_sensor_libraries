import logging

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
            s = "ADXL345: The address (" + str(hex(address)) + ") you entered for the sensor ADXL345 does not exist!"
            if self.consoleLog:
                #print(s)
                logging.error(s)
            s = "ADXL345: Try one of the following:"
            for value in self.poss_addr:
                s = s + str(hex(value)) + " "
            if self.consoleLog:
                #print(s)
                logging.info(s)
                print("ADXL345: not initialized!!!")
                logging.error("ADXL345: not initialized!!!")
    def set_datarate(self, rate):
        try:
            self.poss_datarate.index(rate)
            self.datarate = rate
            self.setDatarate = True
        except ValueError:
            s = "ADXL345: The datarate (" + str(rate) + ") you entered for the sensor ADXL345 does not exist!"
            if self.consoleLog:
                #print(s)
                logging.error(s)
            s = "ADXL345: Try one of the following:"
            for value in self.poss_datarate:
                s = s + str(value) + " "
            if self.consoleLog:
                #print(s)
                logging.info(s)
                #print("ADXL345 datarate not set!!!")
                logging.error("ADXL345 datarate not set!!!")
    def set_range(self, range):
        try:
            self.poss_range.index(range)
            self.range = range
            self.resolution = self.range_resolution[self.poss_range.index(range)]
            self.setRange = True
        except ValueError:
            s = "ADXL345: The range (" + str(range) + ") you entered for the sensor ADXL345 does not exist!"
            if self.consoleLog:
                #print(s)
                logging.error(s)
            s = "ADXL345: Try one of the following:"
            for value in self.poss_range:
                s = s + str(value) + " "
            if self.consoleLog:
                logging.info(s)
                logging.error("ADXL345 range not set!!!")
    def setup(self):
        if self.setAddr and self.setDatarate and self.setRange:
            #all settings correct#
            try:
                self.bus.write_byte_data(self.addr, 0x2C, self.poss_datarate_bin[self.poss_datarate.index(self.datarate)])
                self.bus.write_byte_data(self.addr, 0x2D, 0b00001000)
                self.bus.write_byte_data(self.addr, 0x31, 0b00001011 & self.poss_range_bin[self.poss_range.index(self.range)])
            except OSError as e:
                self.Error = True
                if e.errno == 121:
                    logging.error("ADXL345: Remote I/O Error: The device is not responding on the bus. Therefore it will be ignored")
                else:
                    logging.error(f,"ADXL345: An error occurred: {e}")
                return None
            self.setupD = True
            if self.consoleLog:
                logging.info("ADXL345: Setup finished, sensor ready.")
        else:
            if self.consoleLog:
                logging.error("ADXL345: Setup failed! Settings incorrect")
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
                if self.Error:
                    logging.error("ADXL345: not available")
                else:
                    logging.error("ADXL345: Setup not finished")
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
                if self.Error:
                    logging.error("ADXL345: not available")
                else:
                    logging.error("ADXL345: Setup not finished")
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
                if self.Error:
                    logging.error("ADXL345: not available")
                else:
                    logging.error("ADXL345: Setup not finished")
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
                if self.Error:
                    logging.error("ADXL345: not available")
                else:
                    logging.error("ADXL345: Setup not finished")
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
                if self.Error:
                    logging.error("ADXL345: not available")
                else:
                    logging.error("ADXL345: Setup not finished")
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
                if self.Error:
                    logging.error("ADXL345: not available")
                else:
                    logging.error("ADXL345: Setup not finished")