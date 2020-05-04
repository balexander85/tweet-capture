from configparser import ConfigParser
from pathlib import Path
import os

PROJECT_DIR_PATH = os.path.dirname(__file__)
CONFIG_PATH = str(Path.cwd().joinpath("conf", "config.ini"))

config = ConfigParser()
config.read(CONFIG_PATH)

# Selenium config
CHROME_DRIVER_PATH = config.get("default", "CHROME_DRIVER_PATH")
