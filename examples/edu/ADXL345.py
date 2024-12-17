import time

import structlog

from sts1_sensors import ADXL345

log = structlog.get_logger()

accel = ADXL345(range=2, datarate=50)

while True:
    x, y, z = accel.get_acceleration()
    log.info(f"X: {x:.2f}g, Y: {y:.2f}g, Z: {z:.2f}g")
    time.sleep(.2)
