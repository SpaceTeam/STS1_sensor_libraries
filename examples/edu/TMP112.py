import time
import structlog
from sts1_sensors import TMP112

log = structlog.get_logger()
tmp = TMP112(conversion_rate=1)

while True:
    log.info(f"{tmp.get_temperature():.2f} °C")
    time.sleep(.5)
