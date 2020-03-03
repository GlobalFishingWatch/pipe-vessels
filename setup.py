#!/usr/bin/env python

"""
Setup script for pipe-vessels
"""

from distutils.command.build import build as _build

from setuptools import find_packages
from setuptools import setup

import codecs
import os
import setuptools
import subprocess


package = __import__('pipe_vessels')


DEPENDENCIES = [
    "pytest",
    "nose",
    "ujson",
    "pytz",
    "udatetime",
    "newlinejson",
    "pipe-tools==3.1.0",
    "jinja2-cli",
    "statistics",
    "pyopenssl"
]

with codecs.open('README.md', encoding='utf-8') as f:
    readme = f.read().strip()

with codecs.open('requirements.txt', encoding='utf-8') as f:
    DEPENDENCY_LINKS=[line for line in f]

setup(
    author=package.__author__,
    author_email=package.__email__,
    description=package.__doc__.strip(),
    include_package_data=True,
    install_requires=DEPENDENCIES,
    license="Apache 2.0",
    long_description=readme,
    name='pipe-vessels',
    packages=find_packages(exclude=['test*.*', 'tests']),
    url=package.__source__,
    version=package.__version__,
    zip_safe=True,
    dependency_links=DEPENDENCY_LINKS
)

