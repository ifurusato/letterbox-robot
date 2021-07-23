#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020-2021 by Murray Altheim. All rights reserved. This file is part
# of the Robot Operating System project, released under the MIT License. Please
# see the LICENSE file included as part of this package.
#
# author:   Murray Altheim
# created:  2021-02-25
# modified: 2021-06-13
#
# Just manually turns the HT0740 switch on.
#

import sys, time

from core.logger import Level
from lbr.pir_switch import PirSwitch

try:

    _pin = 24
    _i2c_address = 0x38
    _switch = PirSwitch(_pin, _i2c_address)
    _switch.turn_on_switch()
    time.sleep(10)
    
except Exception as e:
    print('error turning switch on: {}'.format(e))
    sys.exit(1)

