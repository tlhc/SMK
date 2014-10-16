#!/usr/bin/env python
# -*- utf-8 -*-
""" v2login """

import getopt
import sys
import os
import ConfigParser
import urllib
import urllib2
import cookielib
import zlib

import logger
import mail
import v2parser
from HTMLParser import HTMLParseError


def usage():
    """ usage for this script """

    print 'usage: v2login.py -c /path/to/config_file'
    return


class AppException(Exception):
    """ AppException """
    def __init__(self, value):
        self.value = value
        Exception.__init__(self)

    def __str__(self):
        return repr(self.value)


def parsecfg(filename):
    """ parse config file and return config """
    cfg = {}
    if filename is '':
        logger.APPLOGGER.critical('filename is empty')
        return
    if not os.path.isfile(filename):
        logger.APPLOGGER.critical('file invalid')
        return
    with open(filename, 'r') as fhandler:
        try:
            config = ConfigParser.ConfigParser()
            config.readfp(fhandler)
            username = config.get('v2', 'username')
            password = config.get('v2', 'password')
            if username is not '' and password is not '':
                cfg['username'] = username
                cfg['password'] = password
            _mail = config.getint('v2', 'mail')
            cfg['mail'] = _mail
            if _mail == 1:
                fromaddr = config.get('v2', 'fromaddr')
                toaddr = config.get('v2', 'toaddr')
                epass = config.get('v2', 'emailpass')
                smtp = config.get('v2', 'smtp_server')
                cfg['fromaddr'] = fromaddr
                cfg['toaddr'] = toaddr
                cfg['epass'] = epass
                cfg['smtp'] = smtp
        except ConfigParser.Error as ex:
            fhandler.close()
            logger.APPLOGGER.error(ex)

    fhandler.close()
    return cfg

class Request(object):
    """ urllib2 Request """
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/37.0.2062.120 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept-Encoding': 'gzip,deflate',
    }

    def __init__(self):
        cookiejar = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
        urllib2.install_opener(opener)

    def get(self, url, refer):
        """ get """
        req_get = urllib2.Request(url, None, self.headers)
        req_get.add_header('Referer', refer)
        resp = urllib2.urlopen(req_get)
        gziped = resp.headers.get('Content-Encoding')
        req_con = resp.read()
        if gziped:
            req_con = zlib.decompress(req_con, 16 + zlib.MAX_WBITS)
            logger.APPLOGGER.debug('gziped decompress')
        return req_con

    def post(self, url, refer, poststr):
        """ post """
        req_post = urllib2.Request(url, poststr, self.headers)
        req_post.add_header('Referer', refer)
        resp = urllib2.urlopen(req_post)
        gziped = resp.headers.get('Content-Encoding')
        req_con = resp.read()
        # print gziped
        if gziped:
            req_con = zlib.decompress(req_con, 16 + zlib.MAX_WBITS)
            logger.APPLOGGER.debug('gziped decompress')
        return req_con


def main():
    """ login to v2ex and get the coins """
    logger.APPLOGGER.info('init config file parse')
    cfg = {}
    key_user = 'username'
    key_pass = 'password'
    onceval = ''
    req_con = ''

    try:
        optlist, _ = getopt.getopt(sys.argv[1:], 'hc:', ['help', 'config='])
        for opt, arg in optlist:
            if opt == '-c':
                cfg = parsecfg(arg)
            if opt == '-h':
                usage()
                return
    except getopt.GetoptError as ex:
        logger.APPLOGGER.error(ex)

    if key_user not in cfg.keys():
        logger.APPLOGGER.error('username not exists')
        return
    if key_pass not in cfg.keys():
        logger.APPLOGGER.error('password not exists')
        return

    url = 'http://v2ex.com/signin'

    requests = Request()
    if cfg['mail'] == 1:
        email = mail.MailInfo(cfg['smtp'], cfg['fromaddr'],
                              cfg['toaddr'], cfg['epass'], '')

    try:
        req_con = requests.get(url, '')
    except (urllib2.URLError, urllib2.HTTPError) as ex:
        logger.APPLOGGER.error(ex)

    try:
        parser = v2parser.V2HTMLParser()
        parser.feed(req_con)
        onceval = parser.onceval
        parser.close()
        if onceval is '':
            raise AppException('onceval is empty')
    except (HTMLParseError, AppException) as ex:
        logger.APPLOGGER.error(ex)

    try:
        postdata = {}
        postdata['u'] = cfg[key_user]
        postdata['p'] = cfg[key_pass]
        postdata['once'] = onceval
        postdata['next'] = '/'
        poststr = urllib.urlencode(postdata)
        # print poststr
        req_con = requests.post(url, url, poststr)
        if req_con is '':
            raise AppException('req_con is empty')

        gettag = '/mission/daily'
        siteurl = 'http://v2ex.com'
        def getbalance():
            """ get getbalance """
            siteurl = 'http://v2ex.com/balance'

            req_con = requests.get(siteurl, 'http://v2ex.com')
            if req_con is '':
                raise AppException('req_con is empty')

            try:
                parserb = v2parser.V2HTMLParserB()
                parserb.feed(req_con)
                parserb.close()
            except HTMLParseError as ex:
                logger.APPLOGGER.error(ex)

            coins = int(parserb.silver) * 100 + int(parserb.bons)
            logger.APPLOGGER.info('Balance is ' + str(coins) + ' coins')
            return coins

        parserl = v2parser.V2HTMLParserL()
        parserl.feed(req_con)
        parserl.close()

        if parserl.wstatus == 1:
            logger.APPLOGGER.error('logging not success')
            return

        if gettag in req_con:
            _siteurl = siteurl + gettag
            try:
                req_con = requests.get(_siteurl, 'http://v2ex.com')
                if req_con is '':
                    raise AppException('req_con is empty')

                parserx = v2parser.V2HTMLParserX()
                parserx.feed(req_con)
                parserx.close()
                if parserx.finlink is not '':
                    # print parser.finlink
                    try:
                        finlink = siteurl + parserx.finlink

                        req_con = requests.get(finlink, 'http://v2ex.com')
                        if req_con is '':
                            raise AppException('req_con is empty')

                        coins = getbalance()
                        if cfg['mail'] == 1:
                            emsg = 'ID: ' + cfg[key_user] + ' ' \
                                    + 'total coins: ' + str(coins)
                            email.setmsg(emsg)
                            email.send()

                    except (urllib2.HTTPError, AppException) as ex:
                        logger.APPLOGGER.error(ex)

                else:
                    raise AppException('finlink is empty')

            except (urllib2.HTTPError, AppException, HTMLParseError) as ex:
                logger.APPLOGGER.error(ex)
        else:
            logger.APPLOGGER.info('already get coins')
            coins = getbalance()

            if cfg['mail'] == 1:
                emsg = 'already get coins ' + 'ID: ' + cfg[key_user] + ' ' \
                        + 'total coins: ' + str(coins)
                email.setmsg(emsg)
                email.send()

    except urllib2.HTTPError as ex:
        logger.APPLOGGER.error(ex)
        if ex.code == 403:
            if cfg['mail'] == 1:
                emsg = 'ID: ' + cfg[key_user] + ' ' + 'v2ex bian~ '
                email.setmsg(emsg)
                email.send()

if __name__ == '__main__':
    main()
