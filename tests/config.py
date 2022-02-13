"""config.py

Module containing the paths for chromedriver and conf directory
"""
from configparser import ConfigParser
from pathlib import Path

BASE_DIR = Path.cwd()
CONFIG_PATH = str(BASE_DIR.joinpath("tests", "conf", "config.ini"))

config = ConfigParser()
config.read(CONFIG_PATH)

# Selenium config
CHROME_DRIVER_PATH = config.get("default", "CHROME_DRIVER_PATH")
