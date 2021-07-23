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
from enum import Enum
from colorama import init, Fore, Style
init()

from core.logger import Level, Logger

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class Door(Enum):
    OPEN   = ( 0, "open")
    CLOSED = ( 1, "closed")

    # ignore the first param since it's already set by __new__
    def __init__(self, num, name):
        self._name = name

    # this makes sure the name is read-only
    @property
    def name(self):
        return self._name

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class MagneticSwitch(object):
    '''
    Executes a callback upon the change of state of a magnetic contact
    switch connected to a GPIO pin. 

    This returns a Door.OPEN when the door is opened, a Door.CLOSED
    upon it being closed. The closed action includes a second argument
    being the elapsed time that the door was open.

    The switch is pulled high and connected to ground when connected.

    Note that because this is a callback trigger there is no enable/disable
    function, but you should call close() when finished using instances of
    this class.

    :param confif:            the application configuration
    :param doorOpenCallback:  the callback to execute upon door opening
    :param doorCloseCallback: the callback to execute upon door closing
    :param level:             log level
    '''
    def __init__(self, pin, callback, level):
        self._log = Logger("magnetic", level)
        self._pin = pin
        self._callback = callback
        self._log.info('configuring magnetic contact switch on pin {}'.format(self._pin))
        GPIO.setmode(GPIO.BCM)
        # The GPIO pin is set up as an input, pulled up to avoid false
        # detection. The pin is wired to connect to GND as default (magnet
        # engaged), with the door opening disconnecting the magnet and the
        # pin going high.
        #
        # It is configured to detect a rising edge for the door open, a
        # falling edge for the door closing.
        GPIO.setup(self._pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # when a falling edge is detected on the pin, regardless of whatever
        # else is happening in the program, the function _callback will be run
        # 'bouncetime=300' includes the bounce control written into interrupts2a.py
        GPIO.add_event_detect(self._pin, GPIO.BOTH, callback=self._internal_callback, bouncetime=300)
        self._log.info('ready.')

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def _internal_callback(self, value):
        _elapsed_time_sec = 0.0
        _door_state = Door.CLOSED if GPIO.input(self._pin) == 0 else Door.OPEN
        if _door_state is Door.OPEN:
            self._start_time = time.time()
        else:
            _end_time = time.time()
            _elapsed_time_sec = _end_time - self._start_time
        self._log.info('callback on pin: {}; door state: {}; elapsed: {:5.2f} sec'.format(value, _door_state.name, _elapsed_time_sec))
        self._callback(_door_state, _elapsed_time_sec)

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def close(self):
        GPIO.cleanup() # clean up GPIO on normal exit
        self._log.info('closed.')

#EOF
