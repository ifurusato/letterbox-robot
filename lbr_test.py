#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020-2021 by Murray Altheim. All rights reserved. This file is part
# of the Robot Operating System project, released under the MIT License. Please
# see the LICENSE file included as part of this package.
#
# author:   Murray Altheim
# created:  2020-03-16
# modified: 2021-06-11
#
# This tests the PirSwitch class, which reads the state of the PIR sensor
# and turns an HT0740 digital switch on and off.
#

import os, sys, signal, time
from colorama import init, Fore, Style
init()

from lbr.pir_switch import PirSwitch
from core.logger import Logger, Level

# main .........................................................................
def main(argv):
    _log = Logger("lbr-main", Level.INFO)
    _pir = None
    try:
        _log.info('starting letterbox robot...')
        _pin = 24
        _i2c_address = 0x38
        _pir = PirSwitch(_pin, _i2c_address, Level.INFO)
        _log.info(Fore.YELLOW + 'Type ctrl-c to quit...')
        _pir.enable()
        while True:
            _log.debug('pir loop...')
            time.sleep(5.0)
    except KeyboardInterrupt:
        _log.info("caught Ctrl-C.")
    finally:
        _log.info("closing...")
        if _pir:
            _pir.disable()
            _pir.close()

# call main ....................................................................
if __name__== "__main__":
    main(sys.argv[1:])

#EOF
