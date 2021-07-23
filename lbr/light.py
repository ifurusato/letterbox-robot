#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020-2021 by Murray Altheim. All rights reserved. This file is part
# of the Robot Operating System project, released under the MIT License. Please
# see the LICENSE file included as part of this package.
#
# author:   Murray Altheim
# created:  2021-07-23
# modified: 2021-07-23
#

import time
import RPi.GPIO as GPIO
from core.logger import Level, Logger

# ..............................................................................
class Light():
    '''
    Turns the light (a white LED) on and off when it is set enabled or disabled.
    '''
    def __init__(self, config, level):
        self._log = Logger('light', level)
        self._log.debug('initialising...')
        if config is None:
            raise ValueError('no configuration provided.')
        _config = config['ros'].get('light')
        self._led_pin = _config.get('pin')
        self._gpio = GPIO
        self._gpio.setwarnings(False)
        self._gpio.setmode(GPIO.BCM)
        self._gpio.setup(self._led_pin, GPIO.OUT, initial=GPIO.LOW)
        self._log.info('ready.')

    # ..........................................................................
    def enable(self):
        self._log.info('enable.')
        self._gpio.output(self._led_pin, True)

    # ..........................................................................
    def disable(self):
        self._log.info('disable.')
        self._gpio.output(self._led_pin, False)

    # ..........................................................................
    def close(self):
        self.disable()
        self._log.info('closed.')

#EOF
