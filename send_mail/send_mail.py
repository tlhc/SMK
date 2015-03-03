#!/usr/bin/env python
# coding:utf-8
# author TL

""" send mail form list of mail address """

from logger import APPLOGGER
from mail import MailInfo
from AppExp import AppExp
from configreader import MailCfgReader, ConfigObject

def send_signal_section(item):
    """ send a config file content to list of mails """
    def send_file_content(server, fromaddr, toaddr, passwd, msg):
        """ send one cfg file content """
        email = MailInfo(server, fromaddr, toaddr, passwd, msg)
        email.send()
    with open(item.confpath, 'r') as fhander:
        msg = fhander.read()
        [send_file_content(item.smtpserver, \
                item.fromaddress, toaddr, item.emailpwd, msg) \
                for toaddr in item.toaddresslist]

def main():
    cfgparser = MailCfgReader('./mail.cfg')
    allcfg = cfgparser.parser()
    [send_signal_section(item) for item in allcfg]

if __name__ == '__main__':
    main()

