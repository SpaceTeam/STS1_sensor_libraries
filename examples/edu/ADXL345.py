import time

import structlog

from sts1_sensors import ADXL345

log = structlog.get_logger()

accel = ADXL345(range=2, datarate=50)

while True:
    x, y, z = accel.get_g()
    log.info(f"{x=:.2f} g, {y=:.2f} g, {z=:.2f} g")
    time.sleep(.2)