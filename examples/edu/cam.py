import time
import structlog
from sts1_sensors import Camera

cam = Camera()

cam.capture_image("newpic.png")
cam.capture_image("newpic2.png")
custom_settings = {"size": (1920, 1080)}
cam.capture_image_custom(custom_settings, "custom_iamge.png")

cam.capture_sequence("sequence_image", count = 5, interval = 2.0)
