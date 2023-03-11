#!/usr/bin/env python
import sys
from io import open

from setuptools import find_packages, setup

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)

UNSUPPORTED_VERSION_INFO = f'''
==========================
Unsupported Python version
==========================
This version of artifact-hub requires Python {REQUIRED_PYTHON}, but you're trying
to install it on Python {CURRENT_PYTHON}.
This may be because you are using a version of pip that doesn't
understand the python_requires classifier. Make sure you
have pip >= 9.0 and setuptools >= 24.2, then try again:
    $ python -m pip install --upgrade pip setuptools
    $ python -m pip install artifact-hub
This will install the latest version of artifact-hub which works on
your version of Python.
'''

# This check and everything above must remain compatible with Python 2.7.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write(UNSUPPORTED_VERSION_INFO)
    sys.exit(1)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='artifact-hub',
    url='https://https://github.com/robotstech/artifact-hub',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
)
