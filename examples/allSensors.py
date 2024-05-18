import STS1_sensor_libraries as STS1
from smbus2 import SMBus
import time

with SMBus(1) as bus:
    sensors = STS1.main.Sensors(bus)
    #sensors.disable_GUVA_C32()
    sensors.setup()
    while True:
        string = "TempBME: {0:.2f} °C | Hum: {1:.2f} % | Press: {2:.2f} hPa | GasRes:{3:.2f} Ohms | TempTMP: {4:.2f} | GX: {5:.2f} | GY: {6:.2f} | GZ: {7:.2f} | UVA: {8:.2f}"
        val = sensors.getData()
        print(string.format(val.tempBME, val.hum, val.press / 100.0, val.gasRes, val.tempTMP, val.gX, val.gY, val.gZ, val.uva))
        time.sleep(1)
