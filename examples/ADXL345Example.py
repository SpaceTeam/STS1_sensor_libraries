import time
import structlog
from sts1_sensor_libraries import ADXL345

log = structlog.get_logger()

accel = ADXL345(address=0x53, range=2, datarate=3200, 
                x_offset=-0.06, y_offset=0.03, z_offset=0.06)

while True:
    x, y, z = accel.get_g()
    log.info(f"X: {x:.2f}g, Y: {y:.2f}g, Z: {z:.2f}g")
    time.sleep(.2)
