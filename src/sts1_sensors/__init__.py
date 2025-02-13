import structlog

log = structlog.get_logger()

try:
	import libcamera
except ModuleNotFoundError:
	log.warning("'libcamera' is not installed!",
			solution="Run: sudo apt install libcamera-apps python3-libcamera",
			impact="Some functionality may not work correctly.",)
from .edu import *
