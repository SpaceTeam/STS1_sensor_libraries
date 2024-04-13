from smbus2 import i2c_msg
import logging

logging.basicConfig(level=logging.INFO)

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
    Error = False
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
            s = "GUVA_C32: The address (" + str(hex(address)) + ") you entered for the sensor GUVA_C32 does not exist!"
            if self.consoleLog:
                #print(s)
                logging.error(s)
            s = "GUVA_C32: Try one of the following:"
            for value in self.poss_addr:
                s = s + str(hex(value)) + " "
            if self.consoleLog:
                logging.info(s)
                #print(s)
                #print("GUVA_C32 not initialized!!!")
                logging.error("GUVA_C32: not initialized!!!")
    def set_resolution(self, res):
        try:
            self.poss_res.index(res)
            self.res = res
            self.setRes = True
        except ValueError:
            s = "GUVA_C32: The resolution (" + str(hex(address)) + ") you entered for the sensor GUVA_C32 does not exist!"
            if self.consoleLog:
                logging.error(s)
                #print(s)
            s = "GUVA_C32: Try one of the following:"
            for value in self.poss_res:
                s = s + str(hex(value)) + " "
            if self.consoleLog:
                #print(s)
                logging.info(s)
                #print("GUVA_C32 not initialized!!!")
                logging.error("GUVA_C32: not initialized!!!")
    def set_range(self, range_):
        try:
            self.poss_range.index(range_)
            self.range_ = range_
            self.setRange = True
        except ValueError:
            s = "GUVA_C32: The range (" + str(hex(address)) + ") you entered for the sensor GUVA_C32 does not exist!"
            if self.consoleLog:
                #print(s)
                logging.error(s)
            s = "GUVA_C32: Try one of the following:"
            for value in self.poss_range:
                s = s + str(hex(value)) + " "
            if self.consoleLog:
                #print(s)
                logging.info(s)
                #print("GUVA_C32 not initialized!!!")
                logging.error("GUVA_C32: not initialized!!!")
    def setup(self):
        if self.setAddr and self.setRes and self.setRange:
            try:
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
            except OSError as e:
                self.Error = True
                if e.errno == 121:
                    #print("Remote I/O Error: The device is not responding on the bus. Therefore it will be ignored")
                    logging.error("GUVA_C32: Remote I/O Error: The device is not responding on the bus. Therefore it will be ignored")
                else:
                    #print(f"An error occurred: {e}")
                    logging.error(f"GUVA_C32: An error occurred: {e}")
                return None
                    
                
            
            
            self.setupD = True
            if self.consoleLog:
                #print("Setup finished, GUVA_C32 ready.")
                logging.info("GUVA_C32: Setup finished, sensor ready.")
            return True
        else:
            if self.consoleLog:
                #print("Setup failed! Settings incorrect")
                logging.error("GUVA_C32: Setup failed! Settings incorrect")
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
                if self.Error:
                    #print("GUVA_C32 not available")
                    logging.error("GUVA_C32: not available")
                else:
                    #print("Setup not finished")
                    logging.error("GUVA_C32: Setup not finished")
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
                if self.Error:
                    #print("GUVA_C32 not available")
                    logging.error("GUVA_C32: not available")
                else:
                    #print("Setup not finished")
                    logging.error("GUVA_C32: Setup not finished")