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