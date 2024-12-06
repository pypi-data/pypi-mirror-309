#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-

import re
from setuptools import setup, find_packages
from setuptools import *

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('sysinsight/sysinsight.py').read(),
    re.M
    ).group(1)

setup(
    name='system-insight',
    packages=["sysinsight"],
    entry_points = {
        "console_scripts": ["system-insight = sysinsight.sysinsight:main"]
    },
    version=version,
    description='A simple tool for quickly gathering information about the current state of the system.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AquaQuokka/system-insight",
    author="AquaQuokka",
    license='BSD-3-Clause',
    py_modules=['sysinsight'],
    scripts=['sysinsight/sysinsight.py'],
    install_requires=["psutil"],
)
