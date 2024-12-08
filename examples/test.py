from sts1_sensor_libraries import ADXL345
from smbus2 import SMBus
import time

with SMBus(1) as bus:
    ADXL = ADXL345(bus)
    ADXL.set_address(0x53)
    ADXL.set_range(2)
    ADXL.set_datarate(3200)
    ADXL.set_offset(-0.06,0.03,0.06)
    ADXL.setup()
    while True:
        print("X: %.2fg, Y: %.2fg Z: %.2fg" % (ADXL.getXGs(), ADXL.getYGs(), ADXL.getZGs()))
        time.sleep(.1)
