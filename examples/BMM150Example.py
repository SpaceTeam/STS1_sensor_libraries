import STS1_sensor_libraries as STS1
from smbus2 import SMBus
import time

with SMBus(1) as bus:
    BMM = STS1.BMM150(bus)
    BMM.set_address(0x10)
    BMM.set_datarate(10)
    BMM.setup()
    while True:
        print("X: %.2fuT, Y: %.2fuT, Z: %.2fuT" % (BMM.getXuT(), BMM.getYuT(), BMM.getZuT()))
        time.sleep(1)
