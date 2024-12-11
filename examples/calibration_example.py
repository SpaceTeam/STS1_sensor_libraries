from statistics import mean
import time
from sts1_sensor_libraries import ADXL345

accel = ADXL345(address=0x53, range=2, datarate=3200)

measurements = []
for _ in range(500):
    measurements.append(accel.get_g())
    time.sleep(.1)

x_vals, y_vals, z_vals = zip(*measurements)

print(f"suggested x offest: {-mean(x_vals):.5f}")
print(f"suggested y offest: {-mean(y_vals):.5f}")
print(f"suggested z offest: {1-mean(z_vals):.5f}") # we expect z=1
