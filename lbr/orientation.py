#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020-2021 by Murray Altheim. All rights reserved. This file is part
# of the Robot Operating System project, released under the MIT License. Please
# see the LICENSE file included as part of this package.
#
# author:   Murray Altheim
# created:  2019-12-23
# modified: 2020-03-26
#

from enum import Enum

# ..............................................................................
class Orientation(Enum):
    NONE  = ( 0, "none", "none")
    BOTH  = ( 1, "both", "both")
    PORT  = ( 2, "port", "port")
    CNTR  = ( 3, "center", "cntr")
    STBD  = ( 4, "starboard", "stbd")
    PORT_SIDE = ( 5, "port-side", "psid") # only used with infrareds
    STBD_SIDE = ( 6, "stbd-side", "ssid") # only used with infrareds

    # ignore the first param since it's already set by __new__
    def __init__(self, num, name, label):
        self._name = name
        self._label = label

    # this makes sure the name is read-only
    @property
    def name(self):
        return self._name

    # this makes sure the label is read-only
    @property
    def label(self):
        return self._label

#EOF
