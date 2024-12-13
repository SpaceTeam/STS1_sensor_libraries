
import logging
from enum import Enum
import time
from random import randrange



# Enum SensorType
# RADFET           TID measurement sensor
# SRAM             SEE measurement sensor
class SensorType(Enum):
    RADFET  = 0
    SRAM    = 1

# Enum StatusCode
# Ok               Request successful
# InitFailed       Initialization of client library failed
# InvalidCRC       CRC calculation of response failed
# InvalidInput     Invalid input data given
# I2CReadFailed    I2C read request failed
# I2CWriteFailed   I2C write request failed
# DataUnavailable  Measurement data currently unavailable
# NotOperative     SATDOS board not fully operational - if persistent, contact mission operation (TU Wien Space Team)
# TimeNotSet       SATDOS time has not been set since last boot
class StatusCode(Enum):
    Ok              = 0
    InitFailed      = 1
    InvalidCRC      = 2
    InvalidInput    = 3
    I2CReadFailed   = 4
    I2CWriteFailed  = 5
    DataUnavailable = 6
    NotOperative    = 7
    TimeNotSet      = 8

# Structure Response
# Status           Status of request
# Firmware         SATDOS firmware version, applicable only on reqStatus
# Temperature      Temperature value taken from TMP175 sensor, applicable only on reqTemp
# Interval         Sensor interval of the given sensor type, applicable only on reqInterval
# Uptime           Epoch time since last SATDOS boot, applicable only on reqUptime
# RADFET_1         Accumulated Total Dose in units of rad of RADFET 1 sensor since mission start, applicable only on reqTID
# RADFET_2         Accumulated Total Dose in units of rad of RADFET 2 sensor since mission start, applicable only on reqTID
# RADFET_3         Accumulated Total Dose in units of rad of RADFET 3 sensor since mission start, applicable only on reqTID
# RADFET_4         Accumulated Total Dose in units of rad of RADFET 4 sensor since mission start, applicable only on reqTID
# CY62157          Accumulated Single Event Upsets (SEU) on SRAM 1 sensor (= Cypress CY62157) since last readout, applicable only on reqSEE
# ISSI             Accumulated Single Event Upsets (SEU) on SRAM 2 sensor (= ISSI IS61) since last readout, applicable only on reqSEE
class Status:
    Code = StatusCode.Ok
    Message = ""

class response:
    Status      = Status()
    Version     = "Fail"
    Temperature = 0.0
    Interval    = 0.0
    Uptime      = 0.0
    RADFET_1    = 0.0
    RADFET_2    = 0.0
    RADFET_3    = 0.0
    RADFET_4    = 0.0
    CY62157     = 0
    ISSI        = 0

class SatDosClient:
    initialized = False
    response    = None
    interval    = 0
    start_time  = 0
    
    def __init__(self, arg):
        self.response = response()
        if arg == None:
            logging.error("SatDosClient: Parameter wrong.")
        self.start_time = time.time()
            
    def init(self):
        return self.response

    def reqStatus(self):
        response = self.response
        response.Version = "Stub Lib"
        return response
    
    def setInterval(self, sensor_type, interval):
        response = self.response

        if sensor_type not in SensorType:
            response.Status.Code = StatusCode.InvalidInput
            response.Status.Message = "Invalid sensor type"
        elif interval > 3600:
            response.Status.Code = StatusCode.InvalidInput
            response.Status.Message = "Too long interval"
        else:
            self.interval = interval
        return response

    def reqInterval(self, sensor_type):
        response = self.response

        if sensor_type not in SensorType:
            response.Status.Code = StatusCode.InvalidInput
            response.Status.Message = "Invalid sensor type"
        else:
            response.Interval = self.interval
        
        return response

    def reqUptime(self):
        response = self.response
        response.Uptime = time.time() - self.start_time

        return response

    def reqTemp(self):
        response = self.response
        response.Temperature = randrange(-5, 40, 0.01)

        return response

    def reqTID(self):
        response = self.response
        response.RADFET_1 = randrange(0, 40, 0.01)
        response.RADFET_2 = randrange(0, 40, 0.01)
        response.RADFET_3 = randrange(0, 40, 0.01)
        response.RADFET_4 = randrange(0, 40, 0.01)

        return response

    def reqSEE(self):
        response = self.response
        response.CY62157 = randrange(0, 10, 1)
        response.ISSI = randrange(0, 10, 1)

        return response


