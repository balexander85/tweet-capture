"""setup.py

Used for packaging tweetcapture
"""
from pathlib import Path
from setuptools import find_packages, setup


AUTHOR = "Brian Alexander"
AUTHOR_EMAIL = "brian@dadgumsalsa.com"
REPO_URL = "https://github.com/balexander85/tweetcapture"
VERSION = "0.1.5"
DESCRIPTION = "A tool to screenshot tweets with selenium webdriver."

with Path(__file__).parent.joinpath("README.md").open(encoding="UTF-8") as readme:
    README = readme.read()

setup(
    name="tweetcapture",
    version=VERSION,
    packages=find_packages(),
    install_requires=[
        "furl",
        "retry",
        "wrappeddriver @ "
        "git+https://github.com/balexander85/wrappeddriver.git@0.2.6#egg=wrappeddriver",
    ],
    python_requires=">=3.8",
    include_package_data=False,
    license="MIT License",
    description=DESCRIPTION,
    long_description=README,
    url=REPO_URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Selenium",
        "Framework :: Selenium :: 4.1",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
