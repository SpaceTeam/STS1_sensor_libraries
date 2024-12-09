from sts1_sensor_libraries import ADXL345
from smbus2 import SMBus
import time

with SMBus(1) as bus:
    accel = ADXL345(bus, address=0x53, range=2, datarate=3200, 
                    x_offset=-0.06, y_offset=0.03, z_offset=0.06)
    
    while True:
        s = f"X: {accel.get_x_g():.2fg}"
        s += f", Y: {accel.get_y_g():.2fg}"
        s += f", Z: {accel.get_z_g():.2fg}"
        print(s)
        time.sleep(.1)
