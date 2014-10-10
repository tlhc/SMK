#!/usr/bin/env python
# -*- coding utf-8 -*-

""" send mail """
import smtplib
import re

class SendMail(object):

    """ send mail """
    fromaddr = ''
    toaddr = ''
    msg = ''

    def __init__(self):
        pass

    def validaddr(self, address):
        """ valid email """
        patten = r'[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$'
        ret = re.match(patten, address)
        if ret:
            return True
        else:
            return False

    def constructmsg(self, username, conins):
        """ constructmsg """
        self.msg = ''
        if username is '' or conins is '':
            
        self.msg = 'ID: ' + 
