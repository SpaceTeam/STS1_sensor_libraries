import sts1_sensors as STS1
from smbus2 import SMBus
import time

with SMBus(1) as bus:
    gyro = STS1.L3GD20H(bus)
    gyro.set_address(0x6A)
    gyro.set_datarate(50)
    gyro.set_range(2000)
    gyro.setup()
    while True:
        print("X: %.2fdps, Y: %.2fdps Z: %.2fdps" % (gyro.getXdps(), gyro.getYdps(), gyro.getZdps()))
        time.sleep(.1)
