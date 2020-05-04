from configparser import ConfigParser
import os

PROJECT_DIR_PATH = os.path.dirname(__file__)

config = ConfigParser()
config.read(os.path.join(PROJECT_DIR_PATH, "conf", "config.ini"))

# Selenium config
CHROME_DRIVER_PATH = config.get("default", "CHROME_DRIVER_PATH")
