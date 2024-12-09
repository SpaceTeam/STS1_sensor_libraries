
# STS1_sensor_libraries

Streamline the process of handling sensors on the Raspi-Hat / EDU module.

The following sensors are available on the EDU module:
* [`ADXL345`](https://www.analog.com/en/products/adxl345.html) - Digital accelerometer.
* [`BME688`](https://www.bosch-sensortec.com/products/environmental-sensors/gas-sensors/bme688/) - Pressure, humidity, temperature and gas sensor.
* [`BMM150`](https://www.bosch-sensortec.com/products/motion-sensors/magnetometers/bmm150/) - Geomagnetic sensor.
* [`GUVA_C32`](https://www.digikey.de/de/products/detail/genicom-co-ltd/GUVA-C32SM/9960949) - Ultraviolet light sensor.
* [`L3GD20H`](https://www.pololu.com/file/0J731/L3GD20H.pdf) - Three-axis gyroscope.
* [`TMP112`](https://www.ti.com/product/TMP112) - High-accuracy temperature sensor.

## Initial Setup

### Install the Python Package

If you want the latest stable version, install it like so:
```bash
# Recommended
pip install sts1_sensor_libraries
```

If you want the latest development version, install it from the repository url:
```bash
# Not recommended
pip install git+git://github.com/SpaceTeam/STS1_sensor_libraries.git@master
```

### Configure the Package


## Installation for Developers

* Install the [package manager uv](https://docs.astral.sh/uv/getting-started/installation/): `curl -LsSf https://astral.sh/uv/install.sh | sh`
* Add its path to your `~/.bashrc` such that the command `uv` is available.
* Clone this repo: `git clone https://github.com/SpaceTeam/STS1_sensor_libraries`
* Switch into the directory.
* Run `uv sync`. This creates a `.venv` folder and installs all necessary dependencies.
* Run one of the examples: `uv run python examples/ADXL345Example.py`
