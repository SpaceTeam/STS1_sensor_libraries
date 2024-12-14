import time

import structlog

from sts1_sensors import BME688

sensor = BME688()
log = structlog.get_logger()

sensor.enable_gas_measurements = True
sensor.gas_heater_temperature = 320
sensor.gas_heater_duration = 150

for i in range(10):
    t = sensor.get_temperature()
    p = sensor.get_pressure()
    h = sensor.get_humidity()

    heat = sensor.get_heat_stable()
    res = sensor.get_gas_resistance()

    log.info(f"{t:.2f} °C, {p:.2f} hPa, {h:.2f} %RH, {heat=}, {res:.2f} Ohms")
    time.sleep(1)
