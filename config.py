from configparser import ConfigParser
from pathlib import Path

BASE_DIR = Path.cwd().parent
CONFIG_PATH = str(BASE_DIR.joinpath("conf", "config.ini"))

config = ConfigParser()
config.read(CONFIG_PATH)

# Selenium config
CHROME_DRIVER_PATH = config.get("default", "CHROME_DRIVER_PATH")
