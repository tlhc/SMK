#!/usr/bin/env python
# coding:utf-8
# author TL

""" configfile reader """

from os.path import exists, isfile
from ConfigParser import ConfigParser
from ConfigParser import Error as ConfigError
from logger import APPLOGGER
from AppExp import AppExp

class ConfigObject(object):
    """ config object """
    def __init__(self):
        self.confpath = ''
        self.fromaddress = ''
        self.toaddresslist = []
        self.emailpwd= ''
        self.smtpserver= ''

class MailCfgReader(object):
    """ ConfigReader """
    def __init__(self, path):
        self.__path = path
        self.__config = []

    def parser(self):
        """ parse config """
        ava_configlist = []

        def parse_single(confparser, path):
            confobj = ConfigObject()
            confobj.confpath = path
            try:
                if confparser.has_option(path, 'toaddr'):
                    confobj.toaddresslist = [item.strip() \
                            for item in confparser.get(path, 'toaddr').split(',')]
                else:
                    raise AppExp('toaddr read err')
                if confparser.has_option(path, 'fromaddr'):
                    confobj.fromaddress = confparser.get(path, 'fromaddr').strip()
                else:
                    raise AppExp('fromaddr read err')
                if confparser.has_option(path, 'emailpass'):
                    confobj.emailpwd = confparser.get(path, 'emailpass').strip()
                else:
                    raise AppExp('email pass read err')
                if confparser.has_option(path, 'smtp_server'):
                    confobj.smtpserver = confparser.get(path, 'smtp_server').strip()
                else:
                    raise AppExp('smtp server read err')
            except AppExp as ex:
                APPLOGGER.error(ex)
            return confobj

        try:
            if exists(self.__path) and isfile(self.__path):
                with open(self.__path) as fhandler:
                    try:
                        config_parser = ConfigParser()
                        config_parser.readfp(fhandler)
                        ava_configlist = [confs for confs in config_parser.sections() \
                                if MailCfgReader.exist_isfile(confs)]
                        self.__config = [parse_single(config_parser, single) \
                                for single in ava_configlist]
                    except (AppExp, ConfigError) as ex:
                        APPLOGGER.error('read config error')
            else:
                raise AppExp('config file error')
        except OSError as ex:
            APPLOGGER.error(ex)
        return self.__config

    @staticmethod
    def exist_isfile(path):
        """ exist_isfile """
        if exists(path) and isfile(path):
            return True
        return False

    @property
    def config(self):
        """ config object """
        return self.__config
    def __get_path(self):
        """ get path """
        return self.__path
    def __set_path(self, value):
        """ set path """
        self.__path = value
    path = property(__get_path, __set_path)


if __name__ == '__main__':
    """ test function """
    cfgparser = MailCfgReader('./mail.cfg')
    allcfg = cfgparser.parser()
    for item in allcfg:
        print item.confpath
        print item.emailpwd
        print item.fromaddress
        print item.smtpserver
        print item.toaddresslist

