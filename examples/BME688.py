from sts1_sensors import BME688

bme = BME688()
t = bme.get_values()
print(t)
