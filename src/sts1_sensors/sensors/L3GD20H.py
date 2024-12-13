import logging

def twos_comp(val, bits):
    if val & (1 << (bits - 1)) != 0:
        val = val - (1 << bits)
    return val

class L3GD20H:
    poss_addr = [0x6A, 0x6B]
    poss_datarate = [12.5,25,50,100,200,400,800]
    poss_datarate_bin = [0b00, 0b01, 0b10, 0b00, 0b01, 0b10, 0b11]
    poss_LOW_ODR_bin = [0b1, 0b1, 0b1, 0b0, 0b0, 0b0, 0b0]
    poss_range = [245,500,2000]
    poss_range_bin = [0b00, 0b01, 0b10]
    dps_per_digit = [0.00875, 0.01750, 0.07000]

    
    config_set = 0
    addr = 0
    datarate = 0
    range = 0
    
    
    check = 0
    
    setDatarate = False
    setAddr = False
    setupD = False
    Error = False
    consoleLog = True
    setRange = False
    def __init__(self, bus):
        self.addr = 0x6A
        self.bus = bus
    def deact_consoleLog(self):
        self.consoleLog = False
    def set_address(self, address):
        try:
            self.poss_addr.index(address)
            self.addr = address
            self.setAddr = True
        except ValueError:
            s = "L3GD20H: The address (" + str(hex(address)) + ") you entered for the sensor L3GD20H does not exist!"
            if self.consoleLog:
                logging.error(s)
            s = "L3GD20H: Try one of the following:"
            for value in self.poss_addr:
                s = s + str(hex(value)) + " "
            if self.consoleLog:
                logging.info(s)
                logging.error("L3GD20H: not initialized!!!")
    def set_datarate(self, rate):
        try:
            self.poss_datarate.index(rate)
            self.datarate = rate
            self.setDatarate = True
        except ValueError:
            s = "L3GD20H: The datarate (" + str(rate) + ") you entered for the sensor L3GD20H does not exist!"
            if self.consoleLog:
                logging.error(s)
            s = "L3GD20H: Try one of the following:"
            for value in self.poss_datarate:
                s = s + str(value) + " "
            if self.consoleLog:
                logging.info(s)
                logging.error("L3GD20H: datarate not set!!!")
    def set_range(self, range):
        try:
            self.poss_range.index(range)
            self.range = range
            #self.resolution = self.range_resolution[self.poss_range.index(range)]
            self.setRange = True
        except ValueError:
            s = "L3GD20H: The range (" + str(range) + ") you entered for the sensor L3GD20H does not exist!"
            if self.consoleLog:
                logging.error(s)
            s = "L3GD20H: Try one of the following:"
            for value in self.poss_range:
                s = s + str(value) + " "
            if self.consoleLog:
                logging.info(s)
                logging.error("L3GD20H range not set!!!")
    def setup(self):
        if self.setAddr and self.setDatarate and self.setRange:
            #all settings correct
            try:
                #write CTRL1 (datarate, bandwith, powermode and enable for all axis
                self.bus.write_byte_data(self.addr, 0x20, 0b00001111 | (self.poss_datarate_bin[self.poss_datarate.index(self.datarate)] << 6))
                #write CTRL4 (Block Data update, Big/little endian, Full Scale Selection,
                self.bus.write_byte_data(self.addr, 0x23, 0b00000000 | (self.poss_range_bin[self.poss_range.index(self.range)] << 4))
                #write LOW_ODR
                self.bus.write_byte_data(self.addr, 0x39, 0b00000000 | (self.poss_LOW_ODR_bin[self.poss_datarate.index(self.datarate)]))
            except OSError as e:
                self.Error = True
                if e.errno == 121:
                    logging.error("L3GD20H: Remote I/O Error: The device is not responding on the bus. Therefore it will be ignored")
                else:
                    logging.error(f"L3GD20H: An error occurred: {e}")
                return None
 
            self.setupD = True
            if self.consoleLog:
                logging.info("L3GD20H: Setup finished, L3GD20H ready.")
        else:
            if self.consoleLog:
                logging.error("L3GD20H: Setup failed! Settings incorrect")
    def getXraw(self):
        if self.setupD:
            XL_val = self.bus.read_byte_data(0x6a, 0x28)
            XH_val = self.bus.read_byte_data(0x6a, 0x29)
            X_val = (XH_val<<8) + XL_val 
            x = twos_comp(X_val, 16)
            return x
        else:
            if self.consoleLog:
                if self.Error:
                    logging.error("L3GD20H: not available")
                else:
                    logging.error("L3GD20H: Setup not finished")
    def getYraw(self):
        if self.setupD:
            YL_val = self.bus.read_byte_data(0x6A, 0x2A)
            YH_val = self.bus.read_byte_data(0x6a, 0x2B)
            Y_val = (YH_val<<8) + YL_val 
            y = twos_comp(Y_val, 16)
            return y
        else:
            if self.consoleLog:
                if self.Error:
                    logging.error("L3GD20H: not available")
                else:
                    logging.error("L3GD20H: Setup not finished")
    def getZraw(self):
        if self.setupD:
            ZL_val = self.bus.read_byte_data(0x6a, 0x2C)
            ZH_val = self.bus.read_byte_data(0x6a, 0x2D)
            Z_val = (ZH_val<<8) + ZL_val 
            z = twos_comp(Z_val, 16)
            return z
        else:
            if self.consoleLog:
                if self.Error:
                    logging.error("L3GD20H: not available")
                else:
                    logging.error("L3GD20H: Setup not finished")
    def getXdps(self):
        if self.setupD:
            XL_val = self.bus.read_byte_data(0x6a, 0x28)
            XH_val = self.bus.read_byte_data(0x6a, 0x29)
            X_val = (XH_val<<8) + XL_val 
            x = twos_comp(X_val, 16)
            return x * self.dps_per_digit[self.poss_range.index(self.range)]
        else:
            if self.consoleLog:
                if self.Error:
                    logging.error("L3GD20H: not available")
                else:
                    logging.error("L3GD20H: Setup not finished")
    def getYdps(self):
        if self.setupD:
            YL_val = self.bus.read_byte_data(0x6a, 0x2A)
            YH_val = self.bus.read_byte_data(0x6a, 0x2B)
            Y_val = (YH_val<<8) + YL_val 
            y = twos_comp(Y_val, 16)
            return y * self.dps_per_digit[self.poss_range.index(self.range)]
        else:
            if self.consoleLog:
                if self.Error:
                    logging.error("L3GD20H: not available")
                else:
                    logging.error("L3GD20H: Setup not finished")
    def getZdps(self):
        if self.setupD:
            ZL_val = self.bus.read_byte_data(0x6a, 0x2C)
            ZH_val = self.bus.read_byte_data(0x6a, 0x2D)
            Z_val = (ZH_val<<8) + ZL_val 
            z = twos_comp(Z_val, 16)
            return z * self.dps_per_digit[self.poss_range.index(self.range)]
        else:
            if self.consoleLog:
                if self.Error:
                    logging.error("L3GD20H: not available")
                else:
                    logging.error("L3GD20H: Setup not finished")
