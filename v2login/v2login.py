#!/usr/bin/env python
# -*- utf-8 -*-

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

    fomatter = logging.Formatter('%(asctime)s %(levelname)-8s %(funcName)s %(lineno)s %(message)s')
    _logger = logging.getLogger('v2loger')
    _logger.setLevel(logging.DEBUG)
    shandler = logging.StreamHandler()
    fhandler = logging.FileHandler('./v2login.log')
    shandler.setFormatter(fomatter)
    fhandler.setFormatter(fomatter)
    _logger.addHandler(shandler)
    _logger.addHandler(fhandler)
    return _logger


logger = loggerinit()

def parsecfg(filename):
    """ parse config file and return config """
    cfg = {}
    if filename is '':
        logger.critical('filename is empty')
        return
    if not os.path.isfile(filename):
        logger.critical('file invalid')
        return
    with open(filename, 'r') as fp:
        try:
            config = ConfigParser.ConfigParser()
            config.readfp(fp)
            username = config.get('v2', 'username')
            password = config.get('v2', 'password')
            if username is not '' and password is not '':
                cfg['username'] = username
                cfg['password'] = password
        except ConfigParser.Error as ex:
            logger.error(ex)

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
            #print attrs
            for key, val in attrs:
                if gettag in val:
                    spos = val.index(gettag)
                    epos = val.index(';')
                    if epos > spos:
                        self.finlink = val[spos : epos].strip("'")
    def handle_endtag(self, tag):
        pass

class V2HTMLParserB(HTMLParser):
    """ HTMLParser for get balance"""
    def __init__(self):
        self.flagB = 0
        self.flagS = 0
        self.PB = 0
        self.PS = 0
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for key, val in attrs:
                if 'silver' in val:
                    self.flagB = 1

        if tag == 'a':
            for key, val in attrs:
                if 'balance_area' in val:
                    self.flagS = 1

    def handle_endtag(self, tag):
        pass
    def handle_data(self, data):

        if self.flagB == 1:
            # print data.strip()
            self.PB = data.strip()
            self.flagB = 0

        if self.flagS == 1:
            # print data.strip()
            self.PS = data.strip()
            self.flagS = 0


def main():
    """ login to v2ex and get the coins """

    logger.info('init config file parse')
    cfg = {}
    key_user = 'username'
    key_pass = 'password'
    onceval = ''

    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'hc:', ['help', 'config='])
        for opt, arg in optlist:
            if opt == '-c':
                cfg = parsecfg(arg)
            if opt == '-h':
                usage()
                return
    except getopt.GetoptError as ex:
        logger.error(ex)

    if key_user not in cfg.keys():
        logger.error('username not exists')
        return
    if key_pass not in cfg.keys():
        logger.error('password not exists')
        return

    # cj = ''
    # opener = ''
    url = 'http://v2ex.com/signin'

    try:
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
        req = urllib2.Request(url)
        req.add_header('User-Agent',
                       'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36')
        response = urllib2.urlopen(req)
        req_con = response.read()

        # cs = ['%s = %s' % (c.name, c.value) for c in cj]
        # cookies = ';'.join(cs)
    except (urllib2.URLError, urllib2.HTTPError) as ex:
        logger.error(ex)

    try:
        parser = V2HTMLParser()
        parser.feed(req_con)
        onceval = parser.onceval
        parser.close()
        if onceval is '':
            raise Exception('onceval is empty')
    except (HTMLParseError, Exception) as ex:
        logger.error(ex)

    # print onceval
    # print cookies


    try:
        postdata = {}
        postdata['u'] = cfg[key_user]
        postdata['p'] = cfg[key_pass]
        postdata['once'] = onceval
        postdata['next'] = '/'
        poststr = urllib.urlencode(postdata)
        # print poststr
        reqlogin = urllib2.Request(url, poststr)

        reqlogin.add_header('User-Agent',
                            'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36')

        reqlogin.add_header('Content-Type', 'application/x-www-form-urlencoded')
        reqlogin.add_header('Referer', 'http://v2ex.com/signin')
        reqlogin.add_header('Accept-Encoding', 'gzip,deflate')

        resp_login = urllib2.urlopen(reqlogin)
        req_con = resp_login.read()
        gziped = resp_login.headers.get('Content-Encoding')
        # print gziped
        if gziped:
            req_con = zlib.decompress(req_con, 16 + zlib.MAX_WBITS)
            logger.debug('gziped decompress')

        gettag = '/mission/daily'
        siteurl = 'http://v2ex.com'
        if gettag in req_con:
            _siteurl = siteurl + gettag
            try:
                req_get = urllib2.Request(_siteurl)
                req_get.add_header('User-Agent',
                                   'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36')
                req_get.add_header('Content-Type', 'application/x-www-form-urlencoded')
                req_get.add_header('Referer', 'http://v2ex.com')
                req_get.add_header('Accept-Encoding', 'gzip,deflate')
                resp = urllib2.urlopen(req_get)
                gziped = resp.headers.get('Content-Encoding')
                req_con = resp.read()
                if gziped:
                    req_con = zlib.decompress(req_con, 16 + zlib.MAX_WBITS)

                parser = V2HTMLParserX()
                parser.feed(req_con)
                parser.close()
                if parser.finlink is not '':
                    print parser.finlink
                    try:
                        finlink = siteurl + parser.finlink

                        req_get = urllib2.Request(finlink)
                        req_get.add_header('User-Agent',
                                           'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36')
                        req_get.add_header('Content-Type', 'application/x-www-form-urlencoded')
                        req_get.add_header('Referer', 'http://v2ex.com')
                        req_get.add_header('Accept-Encoding', 'gzip,deflate')
                        resp = urllib2.urlopen(req_get)
                        gziped = resp.headers.get('Content-Encoding')
                        req_con = resp.read()
                        if gziped:
                            req_con = zlib.decompress(req_con, 16 + zlib.MAX_WBITS)

                        print req_con
                    except (urllib2.HTTPError) as ex:
                            logger.error(ex)
                else:
                    raise Exception('finlink is empty')

            except (urllib2.HTTPError, Exception) as ex:
                logger.error(ex)
        else:
            logger.info('already get coins')
            siteurl = 'http://v2ex.com/balance'

            req_get = urllib2.Request(siteurl)
            req_get.add_header('User-Agent',
                               'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36')
            req_get.add_header('Content-Type', 'application/x-www-form-urlencoded')
            req_get.add_header('Referer', 'http://v2ex.com')
            req_get.add_header('Accept-Encoding', 'gzip,deflate')
            resp = urllib2.urlopen(req_get)
            gziped = resp.headers.get('Content-Encoding')
            req_con = resp.read()
            if gziped:
                req_con = zlib.decompress(req_con, 16 + zlib.MAX_WBITS)

            parserb = V2HTMLParserB()
            parserb.feed(req_con)
            parserb.close()
            coins = int(parserb.PS) * 100 + int(parserb.PB)
            logger.info('Balance is ' + str(coins) + ' coins')

        # for test
        # print req_con
        # try:
        #     fileh = open('html.html', 'w')
        #     fileh.close()
        #     fileh = open('html.html', 'r+')
        #     fileh.write(req_con)
        #     fileh.close()
        # except IOError as ex:
        #     logger.error(ex)

    except urllib2.HTTPError as ex:
        logger.error(ex)
        if ex.code == 403:
            # send mail
            pass


if __name__ == '__main__':
    main()
