from smbus2 import i2c_msg
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