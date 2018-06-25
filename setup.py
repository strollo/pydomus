#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from setuptools import setup, find_packages
import sys
import warnings

setup(
    name='pydomus',
    version='1.0.3',
    author="Daniele Strollo",
    author_email="daniele.strollo@gmail.com",
    url='http://github.com/strollo/pydomus',
    packages=find_packages(exclude=['tests','samples']),
    description='Lightweight library for IoT sensors communicating via UDP Multicast',
    keywords=["IoT", "Domotics", "Multicasting"],
    platforms=['Windows', 'Linux', 'OSX'],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 1 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: IoT :: SmallComponents',
        'Topic :: IoT :: Cheap HW',
        'Topic :: IoT :: Communication',
    ],
    include_package_data=True,
    license="http://www.apache.org/licenses/LICENSE-2.0",
    zip_safe=False,
)

