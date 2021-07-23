#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020-2021 by Murray Altheim. All rights reserved. This file is part
# of the Robot Operating System project, released under the MIT License. Please
# see the LICENSE file included as part of this package.
#
# author:   Murray Altheim
# created:  2021-02-14
# modified: 2021-06-12
#

import sys, time, threading
import RPi.GPIO as GPIO
from colorama import init, Fore, Style
init()

try:
    from ht0740 import HT0740
except ImportError:
    sys.exit(Fore.RED + "This script requires the ht0740 module.\nInstall with: pip3 install --user ht0740" + Style.RESET_ALL)

from core.logger import Level, Logger

# ..............................................................................
class PirSwitch(object):
    '''
    Uses the state of a PIR sensor connected to a GPIO pin to control 
    the on-off state of an HT0740 digital switch, which can be connected
    to anything but in this case is to a 12 volt strip of white LEDs.

    In a 1 second loop, a counter is incremented if the PIR sensor has
    been triggered, with the count limited to a maximum value. If the
    PIR is not triggered the counter is decremented until it reaches zero.
    If at the end of each loop iteration the value of the count is above 
    zero the HT0740 Switch (and its LED) are turned on, otherwise off (if
    is on).

    :param pin:          the BCM pin to which the PIR sensor is connected
    :param i2c_address:  the I²C address of the HT0740
    :param level:        the log level
    '''
    def __init__(self, pin, i2c_address, switch_tied_to_light=True, level=Level.INFO):
        self._log = Logger("pir", level)
        self._pin         = pin
        self._enabled     = False
        self._count       = 0
        self._count_limit = 10
        self._thread      = None
        self._switch_tied_to_light = switch_tied_to_light
        self._log.info('configuring pir on pin {}'.format(pin))
        # The GPIO pin is set up as an input, pulled low to avoid false
        # detection. The pin is wired to connect to GND on button press.
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # configure the HT0740 digital switch
        try:
#           i2c_address = 0x39 # or modified board
            self._log.info('enabling switch at I²C address 0x{:02X}'.format(i2c_address))
            self._switch = HT0740(i2c_addr=i2c_address)
        except OSError as e:
            self._log.error('error instantiating HT0740: {}. '.format(e) + Fore.YELLOW + 'Is the device available at the specified I²C address?')
            sys.exit(1)
        self._switch.enable()
        self._log.info('ready.')

    # ..........................................................................
    def enable(self):
        self._log.info("enabling pir switch...")
        if not self._switch_tied_to_light:
            self.light(True)
        self._set_active(True)

    # ..........................................................................
    def disable(self):
        self._log.info("disabling pir switch...")
        if not self._switch_tied_to_light:
            self.light(False)
        self._set_active(False)

    # ..........................................................................
    def _set_active(self, active):
        if active:
            if self._thread is None:
                self._log.debug('starting loop...')
                self._enabled = True
                self._thread = threading.Thread(target=PirSwitch.__loop, args=[self, lambda: self._enabled])
                self._thread.start()
            else:
                self._log.warning('ignored: loop already started.')
        else:
            if self._thread is None:
                self._log.debug('ignored: loop thread does not exist.')
            else:
                self._log.info('stop loop...')
                self._enabled = False
                self._thread.join()
                self._thread = None
                self._log.info('loop thread ended.')

    # ..........................................................................
    def __loop(self, f_is_enabled):
        '''
        The PIR-to-HT0740 process thread.
        '''
        while f_is_enabled():
            if self.pir_triggered:
                if self._count == 0:
                    self._count = 5 # power boost
                elif self._count < self._count_limit:
                    self._count += 1
            elif self._count > 0:
                self._count -= 1
            self._log.debug('pir sensor value: ' + Fore.YELLOW + ' {:2d}'.format(self._count))
            # okay, now react to current threshold...
            _switch_is_on = self._switch.switch.state()
            if self._count > 0 and not _switch_is_on:
                self.turn_on_switch()
            elif self._count == 0 and _switch_is_on:
                self.turn_off_switch()
            time.sleep(1.0)
        self._log.info('loop complete.')


    # ..........................................................................
    @property
    def switch_is_on(self):
        '''
        Returns True if the switch is set on.
        '''
        return self._switch.switch.state()

    # ..........................................................................
    def turn_on_switch(self):
        '''
        Turns on the HT0740 Switch as well as the white LED.
        '''
        self._log.info('switch ON.')
        self.switch(True)
        if self._switch_tied_to_light:
            self.light(True)

    # ..........................................................................
    def turn_off_switch(self):
        '''
        Turns off the HT0740 Switch, as well as the white LED.
        '''
        self._log.info('switch OFF.')
        self.switch(False)
        if self._switch_tied_to_light:
            self.light(False)

    # ..........................................................................
    def switch(self, enable):
        if enable:
            self._switch.switch.on()
        else:
            self._switch.switch.off()

    # ..........................................................................
    def light(self, enable):
        if enable:
            self._switch.led.on()
        else:
            self._switch.led.off()

    # ......................................................
    @property
    def pir_triggered(self):
        '''
        Returns True when the PIR sensor is turned on (logic high).
        '''
        return GPIO.input(self._pin)

    # ......................................................
    def close(self):
        self.turn_off_switch()
        GPIO.cleanup() # clean up GPIO on normal exit
        self._log.info('closed.')

#EOF
