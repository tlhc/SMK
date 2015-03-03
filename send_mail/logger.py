#!/usr/bin/env python
# coding:utf-8
# author TL

""" app logger """

import logging

def loggerinit():
    """ init logger """

    fstr = '%(asctime)s %(levelname)-8s %(funcName)s %(lineno)s %(message)s'
    fomatter = logging.Formatter(fstr)
    _logger = logging.getLogger('send_mail')
    _logger.setLevel(logging.DEBUG)
    shandler = logging.StreamHandler()
    fhandler = logging.FileHandler('./send_mail.log')
    shandler.setFormatter(fomatter)
    fhandler.setFormatter(fomatter)
    _logger.addHandler(shandler)
    _logger.addHandler(fhandler)
    return _logger


APPLOGGER = loggerinit()
APPLOGGER.setLevel('INFO')

