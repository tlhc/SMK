#!/usr/bin/env python
# -*- utf-8 -*-
""" v2login """

import getopt
import sys
import os
import logging
import ConfigParser
import urllib
import urllib2
import cookielib
import zlib
from HTMLParser import HTMLParser
from HTMLParser import HTMLParseError


def usage():
    """ usage for this script """

    print 'usage: v2login.py -c /path/to/config_file'
    return


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


class AppException(Exception):
    """ AppException """
    def __init__(self, value):
        self.value = value
        Exception.__init__(self)

    def __str__(self):
        return self.repr(self.value)


def parsecfg(filename):
    """ parse config file and return config """
    cfg = {}
    if filename is '':
        APPLOGGER.critical('filename is empty')
        return
    if not os.path.isfile(filename):
        APPLOGGER.critical('file invalid')
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
        except ConfigParser.Error as ex:
            fhandler.close()
            APPLOGGER.error(ex)

    fhandler.close()
    return cfg


class V2HTMLParser(HTMLParser):
    """ html parser """
    def __init__(self):
        self.onceval = ''
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'input':
            for key, val in attrs:
                if key == 'name' and val == 'once':
                    # print attrs
                    for _key, _val in attrs:
                        if _key == 'value':
                            self.onceval = _val
                            break

    def handle_endtag(self, tag):
        if tag == 'input':
            pass


class V2HTMLParserX(HTMLParser):
    """ HTMLParser for get coins """
    def __init__(self):
        self.finlink = ''
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        gettag = '/mission/daily'
        if tag == 'input':
            # print attrs
            for _, val in attrs:
                if gettag in val:
                    spos = val.index(gettag)
                    epos = val.index(';')
                    if epos > spos:
                        self.finlink = val[spos:epos].strip("'")

    def handle_endtag(self, tag):
        pass


class V2HTMLParserB(HTMLParser):
    """ HTMLParser for get balance"""
    def __init__(self):
        self.flagb = 0
        self.flags = 0
        self.bons = 0
        self.silver = 0
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for _, val in attrs:
                if 'silver' in val:
                    self.flagb = 1

        if tag == 'a':
            for _, val in attrs:
                if 'balance_area' in val:
                    self.flags = 1

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):

        if self.flagb == 1:
            # print data.strip()
            self.bons = data.strip()
            self.flagb = 0

        if self.flags == 1:
            # print data.strip()
            self.silver = data.strip()
            self.flags = 0


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
            APPLOGGER.debug('gziped decompress')
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
            APPLOGGER.debug('gziped decompress')
        return req_con


def main():
    """ login to v2ex and get the coins """
    APPLOGGER.info('init config file parse')
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
        APPLOGGER.error(ex)

    if key_user not in cfg.keys():
        APPLOGGER.error('username not exists')
        return
    if key_pass not in cfg.keys():
        APPLOGGER.error('password not exists')
        return

    url = 'http://v2ex.com/signin'

    requests = Request()
    try:
        req_con = requests.get(url, '')
    except (urllib2.URLError, urllib2.HTTPError) as ex:
        APPLOGGER.error(ex)

    try:
        parser = V2HTMLParser()
        parser.feed(req_con)
        onceval = parser.onceval
        parser.close()
        if onceval is '':
            raise AppException('onceval is empty')
    except (HTMLParseError, AppException) as ex:
        APPLOGGER.error(ex)

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
        if gettag in req_con:
            _siteurl = siteurl + gettag
            try:
                req_con = requests.get(_siteurl, 'http://v2ex.com')
                if req_con is '':
                    raise AppException('req_con is empty')

                parser = V2HTMLParserX()
                parser.feed(req_con)
                parser.close()
                if parser.finlink is not '':
                    print parser.finlink
                    try:
                        finlink = siteurl + parser.finlink

                        req_con = requests.get(finlink, 'http://v2ex.com')
                        if req_con is '':
                            raise AppException('req_con is empty')

                    except (urllib2.HTTPError, AppException) as ex:
                        APPLOGGER.error(ex)

                else:
                    raise AppException('finlink is empty')

            except (urllib2.HTTPError, AppException) as ex:
                APPLOGGER.error(ex)
        else:
            APPLOGGER.info('already get coins')
            siteurl = 'http://v2ex.com/balance'

            req_con = requests.get(siteurl, 'http://v2ex.com')
            if req_con is '':
                raise AppException('req_con is empty')

            parserb = V2HTMLParserB()
            parserb.feed(req_con)
            parserb.close()
            coins = int(parserb.silver) * 100 + int(parserb.bons)
            APPLOGGER.info('Balance is ' + str(coins) + ' coins')

        # for test
        # print req_con
        # try:
        #     fileh = open('html.html', 'w')
        #     fileh.close()
        #     fileh = open('html.html', 'r+')
        #     fileh.write(req_con)
        #     fileh.close()
        # except IOError as ex:
        #     APPLOGGER.error(ex)

    except urllib2.HTTPError as ex:
        APPLOGGER.error(ex)
        if ex.code == 403:
            # send mail
            pass


if __name__ == '__main__':
    main()
