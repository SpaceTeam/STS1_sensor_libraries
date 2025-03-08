[Docs](https://spaceteam.github.io/STS1_sensor_libraries/) | [Github](https://github.com/SpaceTeam/STS1_sensor_libraries) | [PyPI](https://pypi.org/project/sts1-sensors/)

# sts1-sensors

Streamline the process of handling sensors for the STS1 project.

The following sensors are available both on the satellite and **on the EDU module**:
* [`ADXL345`](https://www.analog.com/en/products/adxl345.html) - Digital accelerometer.
* [`BME688`](https://www.bosch-sensortec.com/products/environmental-sensors/gas-sensors/bme688/) - Pressure, humidity, temperature and gas sensor.
* [`BMM150`](https://www.bosch-sensortec.com/products/motion-sensors/magnetometers/bmm150/) - Geomagnetic sensor.
* [`L3GD20H`](https://www.pololu.com/file/0J731/L3GD20H.pdf) - Three-axis gyroscope.
* [`TMP112`](https://www.ti.com/product/TMP112) - High-accuracy temperature sensor.

The following sensors are available **on the satellite only**:
* [`GUVA_C32`](https://www.digikey.de/de/products/detail/genicom-co-ltd/GUVA-C32SM/9960949) - Ultraviolet light sensor.

## Quickstart

```python
from sts1_sensors import ADXL345, BME688, BMM150, L3GD20H, TMP112

# Accelerometer
accel = ADXL345()
x, y, z = accel.get_acceleration()
print(f"{x=:.2f} g, {y=:.2f} g, {z=:.2f} g")

# Temperature, pressure, humidity and gas sensor
multi = BME688(enable_gas_measurements=True)
t = multi.get_temperature()
p = multi.get_pressure()
h = multi.get_humidity()
heat = multi.get_heat_stable()
res = multi.get_gas_resistance()
print(f"{t:.2f} °C, {p:.2f} hPa, {h:.2f} %RH, {heat=}, {res:.2f} Ohms")

# Geomagnetic sensor
mag = BMM150()
x, y, z = mag.get_magnetic_data()
print(f"{x=:.2f} µT, {y=:.2f} µT, {z=:.2f} µT")
print(f"Heading: {mag.get_heading():.2f}°")

# Gyroscope
gyro = L3GD20H()
x, y, z = gyro.get_angular_momentum()
print(f"{x=:.2f} dps, {y=:.2f} dps, {z=:.2f} dps")

# Temperature sensor
temp = TMP112()
print(f"{temp.get_temperature():.2f} °C")
```
More examples, see examples folder.

## Installation

### Initial Setup on the Raspberry Pi

* Open a terminal on the Raspberry Pi (e.g. via SSH).
* [Activate the I2C interface](https://www.raspberrypi-spy.co.uk/2014/11/enabling-the-i2c-interface-on-the-raspberry-pi/): `sudo raspi-config`
* Reboot `sudo reboot now` then reconnect.
* Run `sudo apt-get install i2c-tools`
* Run `ls /dev/i2c*`. Note the last number that apprears. E.g. for `/dev/i2c-1` this would be `1`.
* Run `i2cdetect -y 1`. You may change that last number according to what you saw in the previous step.
* If you see a grid of dashes `--` with some numbers, this means some sensors were recognized and you are good to go. For example:
```
flo@raspberrypi:~ $ sudo i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:                         -- -- -- -- -- -- -- --
10: 10 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- 48 -- -- -- -- -- -- --
50: -- -- -- 53 -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- 6a -- -- -- -- --
70: -- -- -- -- -- -- 76 --
```

### Installing the Python Package on the Raspberry Pi
Before installing this library, make sure `picamera2` is installed system-wide:  
```bash
sudo apt install python3-picamera2
```

If you want the latest stable version of the senor libray, install it like so:
```bash
pip install sts1-sensors
```

Depending on the Raspberry Pi OS version you are using it may be necessary to install the library in a python virtual environment
```bash
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
pip install sts1-sensors
```

> **🚨 Note:** This library has only been tested with the **Arducam IMX519** camera module ([link](https://www.uctronics.com/arducam-mini-16mp-imx519-camera-module-raspberry-pi-zero.html)).  
> Camera-specific setup steps are required before use.  
> Here are the steps required for the **Arducam IMX519** ([link](https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/16MP-IMX519/))
## For Developers

* Install [just](https://github.com/casey/just?tab=readme-ov-file#pre-built-binaries): `curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to ~/bin`
* Add it to `~/.bashrc`: `export PATH="$PATH:$HOME/bin"`
* Install the [package manager uv](https://docs.astral.sh/uv/getting-started/installation/): `curl -LsSf https://astral.sh/uv/install.sh | sh`
* Add its path to your `~/.bashrc` such that the command `uv` is available: `export PATH=$HOME/.local/bin:$PATH`
* Clone this repo: `git clone https://github.com/SpaceTeam/STS1_sensor_libraries`
* Switch into the directory.
* Run `uv sync --all-extras --dev`. This creates a `.venv` folder and installs all necessary dependencies.
* (Only on Raspberry Pi) Run `pytest`

## Acknowledgments

This project makes use of the following open-source libraries and resources:

* [bmm150](https://gitlab.com/umoreau/bmm150) - Usage of the bmm150 sensor.
* [bme680](https://github.com/pimoroni/bme680-python) - Usage of the bme680 sensor.
