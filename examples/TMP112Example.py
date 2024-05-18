import STS1_sensor_libraries as STS1
from smbus2 import SMBus
import time

with SMBus(1) as bus:
    TMP = STS1.TMP112(bus)
    TMP.set_mode(0)
    TMP.set_address(0x48)
    TMP.set_conversionrate(8)
    TMP.setup()
    while True:
        print("%.2f °C" % (TMP.getTemp()))
        time.sleep(.1)
