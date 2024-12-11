[Github](https://github.com/SpaceTeam/STS1_sensor_libraries) | [PyPI](https://pypi.org/project/sts1-sensor-libraries/)

# sts1-sensor-libraries

Streamline the process of handling sensors on the Raspi-Hat / EDU module.

The following sensors are available on the EDU module:
* [`ADXL345`](https://www.analog.com/en/products/adxl345.html) - Digital accelerometer.
* [`BME688`](https://www.bosch-sensortec.com/products/environmental-sensors/gas-sensors/bme688/) - Pressure, humidity, temperature and gas sensor.
* [`BMM150`](https://www.bosch-sensortec.com/products/motion-sensors/magnetometers/bmm150/) - Geomagnetic sensor.
* [`GUVA_C32`](https://www.digikey.de/de/products/detail/genicom-co-ltd/GUVA-C32SM/9960949) - Ultraviolet light sensor.
* [`L3GD20H`](https://www.pololu.com/file/0J731/L3GD20H.pdf) - Three-axis gyroscope.
* [`TMP112`](https://www.ti.com/product/TMP112) - High-accuracy temperature sensor.


## Initial Setup on the Raspberry Pi

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

## Installing the Python Package on the Raspberry Pi

If you want the latest stable version, install it like so:
```bash
pip install sts1-sensor-libraries
```

## Installation for Package Developers

* Install [just](https://github.com/casey/just?tab=readme-ov-file#pre-built-binaries)
* Install the [package manager uv](https://docs.astral.sh/uv/getting-started/installation/): `curl -LsSf https://astral.sh/uv/install.sh | sh`
* Add its path to your `~/.bashrc` such that the command `uv` is available: `export PATH=$HOME/.local/bin:$PATH`
* Clone this repo: `git clone https://github.com/SpaceTeam/STS1_sensor_libraries`
* Switch into the directory.
* Run `uv sync`. This creates a `.venv` folder and installs all necessary dependencies.
* Run one of the examples: `uv run python examples/ADXL345_example.py`
