#!/usr/bin/env python
# -*- utf-8 -*-

""" app logger """

import logging

def loggerinit():
    """ init logger """

    fstr = '%(asctime)s %(levelname)-8s %(funcName)s %(lineno)s %(message)s'
    fomatter = logging.Formatter(fstr)
    _logger = logging.getLogger('v2loger')
    _logger.setLevel(logging.DEBUG)
    shandler = logging.StreamHandler()
    fhandler = logging.FileHandler('./v2login.log')
    shandler.setFormatter(fomatter)
    fhandler.setFormatter(fomatter)
    _logger.addHandler(shandler)
    _logger.addHandler(fhandler)
    return _logger


APPLOGGER = loggerinit()
APPLOGGER.setLevel('INFO')

