#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020-2021 by Murray Altheim. All rights reserved. This file is part
# of the Robot Operating System project, released under the MIT License. Please
# see the LICENSE file included as part of this package.
#
# author:   Murray Altheim
# created:  2019-12-23
# modified: 2020-03-12
#
# See: https://setuptools.readthedocs.io/en/latest/userguide/index.html
#      https://setuptools.readthedocs.io/en/latest/userguide/quickstart.html
#

from setuptools import setup

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='letterbox-robot',
    version='0.0.7',  # Use bumpversion!
    description="Robot Operating System - Letterbox Robot",
    long_description=long_description,
    author='Ichiro Furusato',
    author_email='ichiro.furusato@gmail.com',
    packages=['letterbox-robot'],
    include_package_data=True,
    install_requires=[
        'colorama',
        'pyyaml',
        'python-daemon'
    ],
    zip_safe=False,
    url='https://github.com/ifurusato/letterbox-robot',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Other OS',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Topic :: Robot Framework',
        'Topic :: Robot Framework :: Library',
        'Topic :: Robot Framework :: Tool',
    ],
)
# future requries:
#   'rpi.gpio', \
#   'adafruit-extended-bus', \
#   'pymessagebus==1.*', \
#   'ht0740', \
#   'pimoroni-ioexpander', \
#   'adafruit-circuitpython-bno08x', \
#   'matrix11x7', \
#   'rgbmatrix5x5', \
