from sts1_sensor_libraries import ADXL345
from smbus2 import SMBus
import time

with SMBus(1) as bus:
    accel = ADXL345(bus)
    accel.set_address(0x53)
    accel.set_range(2)
    accel.set_datarate(3200)
    accel.set_offset(-0.06, 0.03, 0.06)
    accel.setup()
    while True:
        s = f"X: {accel.getXGs():.2fg}"
        s += f", Y: {accel.getYGs():.2fg}"
        s += f", Z: {accel.getZGs():.2fg}"
        print(s)
        time.sleep(.1)
