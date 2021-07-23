#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020-2021 by Murray Altheim. All rights reserved. This file is part
# of the Robot Operating System project, released under the MIT License. Please
# see the LICENSE file included as part of this package.
#
# author:   Murray Altheim
# created:  2020-08-01
# modified: 2021-06-20
#
# Daemon for the Letterbox Robot (lbrd). This also uses the lbrd.service.
#
# see: https://dpbl.wordpress.com/2017/02/12/a-tutorial-on-python-daemon/
# ..............................................................................

import sys
try:
    import daemon
    from daemon import pidfile
except Exception:
    sys.exit("This script requires the python-daemon module.\nInstall with: pip3 install --user python-daemon")
from pathlib import Path
import os, time, traceback
from datetime import datetime

from core.config_loader import ConfigLoader
from lbr.pir_switch import PirSwitch
from core.logger import Logger, Level

PIDFILE = '/home/pi/letterbox-robot/.lbrd.pid'

# ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
def shutdown(signum, frame):  # signum and frame are mandatory
    sys.exit(0)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class LetterboxRobotDaemon():
    '''
    The daemon controlling the Letterbox Robot (PirSwitch) application.
    '''
    def __init__(self, config, level):
        self._log = Logger("lbrd", level)
        self._log.info('initialising letterbox robot daemon...')
        if config is None:
            raise ValueError('no configuration provided.')
        self._log.info('configuration provided.')
        self._config = config
#       _toggle_pin  = self._config.get('toggle_pin')
        # TODO
        _pin = 24
        _i2c_address = 0x38
        self._pir = PirSwitch(_pin, _i2c_address, Level.INFO)

        # OS considerations ..........................
        _rosd_mask = os.umask(0)
        os.umask(_rosd_mask)
        self._log.info('mask: {}'.format(_rosd_mask))
        self._log.info('uid:  {}'.format(os.getuid()))
        self._log.info('gid:  {}'.format(os.getgid()))
        self._log.info('cwd:  {}'.format(os.getcwd()))
        self._log.info('pid file: {}'.format(PIDFILE))
        # configured features ..........................
        self._set_pi_leds(False)
        self._log.info('lbrd ready.')

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def _get_timestamp(self):
        return datetime.utcfromtimestamp(datetime.utcnow().timestamp()).isoformat()

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def _set_pi_leds(self, enable):
        '''
        Enables or disables the Raspberry Pi's board LEDs.
        '''
        _sudo_name  = self._config['pi'].get('sudo_name')
        _led_0_path = self._config['pi'].get('led_0_path')
        _led_0 = Path(_led_0_path)
        _led_1_path = self._config['pi'].get('led_1_path')
        _led_1 = Path(_led_1_path)
        if _led_0.is_file() and _led_0.is_file():
            if enable:
                self._log.info('re-enabling LEDs...')
                os.system('echo 1 | {} tee {}'.format(_sudo_name,_led_0_path))
                os.system('echo 1 | {} tee {}'.format(_sudo_name,_led_1_path))
            else:
                self._log.info('disabling LEDs...')
                os.system('echo 0 | {} tee {}'.format(_sudo_name,_led_0_path))
                os.system('echo 0 | {} tee {}'.format(_sudo_name,_led_1_path))
        else:
            self._log.warning('could not change state of LEDs: does not appear to be a Raspberry Pi.')

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def enable(self):
        self._pir.enable()
        self._log.info('🍏 letterbox robot daemon enabled at: {}'.format(self._get_timestamp()))

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def disable(self):
        self._pir.disable()

    # ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
    def close(self):
        self._pir.disable()
        self._pir.close()
        self._set_pi_leds(True)
        self._log.info('🍎 letterbox robot daemon closed at: {}'.format(self._get_timestamp()))

# ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
def main():

    _daemon = None

    _log = Logger("main", Level.INFO)
    _log.info('starting up...')

    try:
        _loader = ConfigLoader(Level.INFO)
        filename = 'config.yaml'
        _config = _loader.configure(filename)
        _daemon = LetterboxRobotDaemon(_config, Level.INFO)
        _daemon.enable()
        while True:
            _log.debug('main loop...')
            time.sleep(5.0)

    except KeyboardInterrupt:
        _log.info("caught Ctrl-C.")
    except Exception:
        print('error starting lbrd daemon: {}'.format(traceback.format_exc()))
    finally:
        _log.info("closing...")
        if _daemon:
            try:
                _daemon.close()
            except Exception:
                print('error closing lbrd daemon.')
        print('lbrd complete.')

# ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
with daemon.DaemonContext(
    stdout=sys.stdout,
    stderr=sys.stderr,
#   chroot_directory=None,
    working_directory='/home/pi/letterbox-robot',
    umask=0o002,
    pidfile=pidfile.TimeoutPIDLockFile(PIDFILE), ) as context:
#   signal_map={
#       signal.SIGTERM: shutdown,
#       signal.SIGTSTP: shutdown
#   }) as context:
    main()

#EOF
