from sts1_sensors import BMM150

mag = BMM150()
x, y, z = mag.read_mag_data()
degrees = mag.get_heading()

print(f"{x=}, {y=}, {z=}")
print(f"Heading: {degrees:.2f}°")
