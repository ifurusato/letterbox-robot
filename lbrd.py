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

import os, time, traceback
from datetime import datetime

from core.config_loader import ConfigLoader
from lbr.pir_switch import PirSwitch
from core.logger import Logger, Level

PIDFILE = '/home/pi/letterbox-robot/.lbrd.pid'

# ..............................................................................

def shutdown(signum, frame):  # signum and frame are mandatory
    sys.exit(0)

# ..............................................................................
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
#       self._config = config['lbrd']
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
        self._log.info('lbrd ready.')

    # ..........................................................................
    def _get_timestamp(self):
        return datetime.utcfromtimestamp(datetime.utcnow().timestamp()).isoformat()

    # ..........................................................................
    def enable(self):
        self._pir.enable()
        self._log.info('🍏 letterbox robot daemon enabled at: {}'.format(self._get_timestamp()))

    # ..........................................................................
    def disable(self):
        self._pir.disable()

    # ..........................................................................
    def close(self):
        self._pir.disable()
        self._pir.close()
        self._log.info('🍎 letterbox robot daemon closed at: {}'.format(self._get_timestamp()))

# main .........................................................................

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

# ..............................................................................

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
