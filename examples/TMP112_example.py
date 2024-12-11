import time
import structlog
from sts1_sensor_libraries import TMP112

log = structlog.get_logger()
tmp = TMP112(address=0x48, conversion_rate=1)

while True:
    log.info(f"{tmp.get_temp():.2f} °C")
    time.sleep(.5)
