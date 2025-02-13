import time
import os
from picamera2 import Picamera2

class Camera:
    def __init__(self):
        """
        Initializes the camera.
        """
        self.picam2 = Picamera2()
        os.makedirs("results", exist_ok=True)
        
    def capture_image(self, filename: str):
        """
        Captures an image with default settings and saves it to the 'results' fodler.
        """
        self.picam2.start()
        time.sleep(1)
        self.picam2.capture_file(os.path.join("results", filename))
        self.picam2.stop()
        time.sleep(1)

    def capture_image_custom(self, settings: dict, filename: str):
        """
        Captures an image with custom settings and saves it to the 'results' folder.
        :param settings: Dictionary with custom settings (e.g., resolution, exposure time).
        :param filename: Name of the file to save.
        """
        self.picam2.configure(self.picam2.create_still_configuration(raw=settings))
        self.picam2.start()
        time.sleep(1)
        self.picam2.capture_file(os.path.join("results", filename))
        self.picam2.stop()
        time.sleep(1)
    
    def capture_sequence(self, file_prefix: str, count: int, interval: float = 1.0):
        """
        Captures a sequence of images with a set interval between captures.
        :param file_prefix: Prefix for the saved images.
        :param count: Number of images to take.
        :param interval: Delay in seconds between captures (default is 1 sec).
        """
        self.picam2.start()
        time.sleep(1)  # Allow camera to stabilize
        
        for i in range(count):
            filename = f"{file_prefix}_{i+1}.jpg"
            self.picam2.capture_file(os.path.join("results", filename))
            if i < count - 1:
                time.sleep(interval)
        
        self.picam2.close()
        time.sleep(1)
