from statistics import mean
import time
from sts1_sensors import ADXL345

accel = ADXL345(range=2, datarate=50)

measurements = []
# takes 40 secs
for _ in range(200):
    measurements.append(accel.get_g())
    time.sleep(.2)

x_vals, y_vals, z_vals = zip(*measurements)

print(f"suggested x offest: {-mean(x_vals):.5f}")
print(f"suggested y offest: {-mean(y_vals):.5f}")
print(f"suggested z offest: {1-mean(z_vals):.5f}") # we expect z=1
