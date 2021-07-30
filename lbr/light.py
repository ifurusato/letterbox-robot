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
        self._pwm = None
        self._log.info('ready.')

    # ..........................................................................
    def enable(self):
        '''
        Turns on the light at full brightness.
        '''
        self._log.info('enable.')
        self._gpio.output(self._led_pin, True)

    # ..........................................................................
    def pwm(self, duty_cycle):
        '''
        Turns on the light at partial brightness using PWM.
        '''
        if self._pwm:
            self._log.warn('PWM already enabled.')
        else:
            self._pwm = GPIO.PWM(self._led_pin, 100) # initialize PWM at 100Hz frequency
            self._pwm.start(0) # Start PWM with 0% duty cycle
            self._pwm.ChangeDutyCycle(duty_cycle)
            self._log.info('PWM enabled at {:d} duty cycle.'.format(duty_cycle))

    # ..........................................................................
    def disable(self):
        '''
        Turns off the light.
        '''
        if self._pwm is not None:
            self._pwm.stop()
        else:
            self._gpio.output(self._led_pin, False)
        self._log.info('disabled.')

    # ..........................................................................
    def close(self):
        self.disable()
        self._log.info('closed.')

#EOF
