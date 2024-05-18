import STS1_sensor_libraries as STS1
from smbus2 import SMBus
import time

with SMBus(1) as bus:
    ADXL = STS1.ADXL345(bus)
    ADXL.set_address(0x53)
    ADXL.set_datarate(12.5)
    ADXL.set_range(16)
    ADXL.setup()
    while True:
        print("X: %.2fg, Y: %.2fg Z: %.2fg" % (ADXL.getXGs(), ADXL.getYGs(), ADXL.getZGs()))
        time.sleep(.1)
