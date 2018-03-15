#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from setuptools import setup, find_packages
import sys
import warnings

version = 0.1

setup(
    name='pymulticomm',
    version=0.1,
    author='Daniele Strollo',
    author_email='daniele.strollo@gmail.com',
    url='http://github.com/strollo/pydomotz',
    packages=find_packages(),
    scripts=[],
    install_requires=dynamic_requires,
    description='Lightweight multicast communication overlay library',
    classifiers=[
        'Development Status :: 1 - Beta',
        'Intended Audience :: Developers - Nerds - Cat lovers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    include_package_data=True,
    zip_safe=False,
)
