#!/usr/bin/env python
# coding:utf-8
# author TL

""" send mail utils """

import re
import logger
import smtplib
from email.mime.text import MIMEText

class MailInfo(object):

    """ send mail cls"""
    def __init__(self, server, fromaddr, toaddr, password, msg):
        self.server = server
        self.fromaddr = fromaddr
        self.toaddr = toaddr
        self.password = password
        self.msg = msg

    @classmethod
    def validaddr(cls, addr):
        """ valid email """
        patten = r'[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$'
        ret = re.match(patten, addr)
        if ret:
            return True
        else:
            return False

    def __genmsg(self):
        """ gen mail msg"""
        _msg = MIMEText(self.msg)
        _msg['Subject'] = 'shadowsocks config info'
        _msg['From'] = self.fromaddr
        _msg['To'] = self.toaddr
        self.msg = _msg.as_string()

    def setmsg(self, msg):
        """ gen msg """
        self.msg = msg
        self.__genmsg()
        return

    def send(self):
        """ send function """
        if self.validaddr(self.fromaddr) and self.validaddr(self.toaddr):
            self.__genmsg()
            try:
                target = smtplib.SMTP(self.server, 25)
                #target.set_debuglevel(1)
                target.login(self.fromaddr, self.password)
                target.sendmail(self.fromaddr, self.toaddr, self.msg)
                target.close()
                logger.APPLOGGER.info('mail send')
            except smtplib.SMTPException as ex:
                logger.APPLOGGER.error(ex)
        return

