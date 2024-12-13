from sts1_sensors import BMM150

mag = BMM150()
x, y, z = mag.get_magnetic_data()
print(f"{x=:.2f} µT, {y=:.2f} µT, {z=:.2f} µT")

degrees = mag.get_heading()
print(f"Heading: {degrees:.2f}°")

