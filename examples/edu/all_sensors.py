import time

import structlog
from sts1_sensors import ADXL345, BME688, BMM150, L3GD20H, TMP112

log = structlog.get_logger()

accel = ADXL345() # Accelerometer
mag = BMM150() # Geomagnetic sensor
gyro = L3GD20H() # Gyroscope
temp = TMP112() # Temperature sensor
multi = BME688(enable_gas_measurements=True) # Pressure, humidity, temperature and gas sensor

for _ in range(10):
    gx, gy, gz = accel.get_acceleration()
    s = f"{gx=:.2f}, {gy=:.2f}, {gz=:.2f}"
    
    mx, my, mz = mag.get_magnetic_data()
    s += f", {mx=:.2f} µT, {my=:.2f} µT, {mz=:.2f} µT"
    s += f", Heading: {mag.get_heading():.2f}°"

    px, py, pz = gyro.get_angular_momentum()
    s += f", {px=:.2f} dps, {py=:.2f} dps, {pz=:.2f} dps"

    t1 = temp.get_temperature() 
    s += f", temp1 {t1:.2f} °C"

    t2 = multi.get_temperature()
    p = multi.get_pressure()
    h = multi.get_humidity()
    heat = multi.get_heat_stable()
    res = multi.get_gas_resistance()
    s += f", temp2 {t2:.2f} °C, {p:.2f} hPa, {h:.2f} %RH, {heat=}, {res:.2f} Ohms"
    
    log.info(s)
    time.sleep(2)
