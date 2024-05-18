from setuptools import setup, find_packages

setup(
    name="STS1_sensor_libraries",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "smbus2"
    ],
    author="Simon Köfinger",
    author_email="simon.koefinger@spaceteam.at",
    description="A sensor library for the CubeSat STS1 (TU Wien Space Team)"
)
