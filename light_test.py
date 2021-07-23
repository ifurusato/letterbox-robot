#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 by Murray Altheim. All rights reserved. This file is part of
# the Robot Operating System project and is released under the "Apache Licence,
# Version 2.0". Please see the LICENSE file included as part of this package.
#
# author:   Murray Altheim
# created:  2019-12-23
# modified: 2021-03-24
#

import sys, time, traceback
from colorama import init, Fore, Style
init()

from core.config_loader import ConfigLoader
from core.logger import Level
from lbr.light import Light

# main .........................................................................

def main(argv):

    _light = None

    try:
        # read YAML configuration
        _loader = ConfigLoader(Level.INFO)
        _config = _loader.configure('config.yaml')

        _light = Light(_config, Level.INFO)
        _light.enable()

        while True:
            time.sleep(1.0)

    except KeyboardInterrupt:
        print(Fore.CYAN + Style.BRIGHT + 'caught Ctrl-C; exiting...')
    except Exception:
        print(Fore.RED + Style.BRIGHT + 'error starting ros: {}'.format(traceback.format_exc()) + Style.RESET_ALL)
    finally:
        if _light is not None:
            _light.close()

# call main ....................................................................
if __name__== "__main__":
    main(sys.argv[1:])

#EOF
