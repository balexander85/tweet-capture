import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="tweet_capture",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "selenium",
        "furl",
        "retry",
        "pytest",
        "WrappedDriver @ git+https://github.com/balexander85/WrappedDriver.git#egg=WrappedDriver",
    ],
    dependency_links=[
        "git+https://github.com/balexander85/WrappedDriver.git#egg=WrappedDriver"
    ],
    include_package_data=False,
    license="MIT License",
    description="A simple wrapper for selenium webdriver.",
    long_description=README,
    url="https://github.com/balexander85/tweet_capture",
    author="Brian Alexander",
    author_email="brian@dadgumsalsa.com",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Selenium",
        "Framework :: Selenium :: 3.1",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
