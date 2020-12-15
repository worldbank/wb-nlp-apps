import pathlib
from setuptools import setup, find_packages

BASE_DIR = pathlib.Path(__file__).parent

PACKAGE_NAME = 'nlp_api'
VERSION = '0.0.01'
AUTHOR = 'Aivin V. Solatorio'
URL = 'https://github.com/avsolatorio/wb_nlp/app/nlp_api'

LICENSE = 'MIT'
DESCRIPTION = 'Python API'

INSTALL_REQUIRES = ['fastapi']


# Setting up
setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR,
    url=URL,
    description=DESCRIPTION,
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(include=['wb_nlp'])
)
