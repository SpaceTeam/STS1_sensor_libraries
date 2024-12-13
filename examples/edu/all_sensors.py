import time

import structlog
from sts1_sensors import ADXL345, BMM150, L3GD20H, TMP112

log = structlog.get_logger()

accel = ADXL345() # Accelerometer
mag = BMM150() # Geomagnetic sensor
gyro = L3GD20H() # Gyroscope
temp = TMP112() # Temperature sensor

for _ in range(10):
    gx, gy, gz = accel.get_g()
    s = f"{gx=:.2f}, {gy=:.2f}, {gz=:.2f}"
    
    mx, my, mz = mag.get_magnetic_data()
    s += f", {mx=:.2f} µT, {my=:.2f} µT, {mz=:.2f} µT"
    s += f", Heading: {mag.get_heading():.2f}°"

    px, py, pz = gyro.get_position()
    s += f", {px=:.2f} dpfs, {py=:.2f} dpfs, {pz=:.2f} dpfs"

    t = temp.get_temp() 
    s += f", {t:.2f} °C"

    log.info(s)
    time.sleep(2)
