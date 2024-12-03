
from distutils.core import setup
from os import path

from setuptools import find_packages

from src import (
    __author__,
    __author_email__,
    __description__,
    __name__,
    __repo__,
    __version__,
)


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(path.join(this_directory, "requirements.txt"), encoding="utf-8") as f:
    required = f.read().splitlines()

setup(
    name=__name__,
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    packages=find_packages(),
    url=__repo__,
    description=__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=required,
)
