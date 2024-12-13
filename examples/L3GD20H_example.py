import time
import structlog
from sts1_sensors import L3GD20H

log = structlog.get_logger()

gyro = L3GD20H(range=245, datarate=12.5)

while True:
    x, y, z = gyro.get_position()
    log.info(f"X: {x:.2f}dpfs, Y: {y:.2f}dpfs, Z: {z:.2f}dpfs")
    time.sleep(.25)
