#!/usr/bin/env python
# -*- utf-8 -*-
""" v2ex html parser """
from HTMLParser import HTMLParser

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
            # tmplist = [finval for key, val in attrs
            #                     if key == 'name' and val == 'once'
            #                   for _key, finval in attrs
            #                     if _key == 'value']
            # if len(tmplist) == 1:
            #    self.onceval = str(tmplist)

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
        self.flagb = self.flags = self.flagg = 0
        self.bons = self.silver = self.gold = 0
        self.isg = self.iss = 0
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for _, val in attrs:
                if 'balance_area' in val:
                    self.flagg = self.flags = self.flagb = 1

        if tag == 'img':
            for _, val in attrs:
                if 'gold' in val:
                    self.flags = self.isg = 1
                if 'silver' in val:
                    self.flagb = self.iss = 1

    def handle_endtag(self, tag):
        if tag == 'html':
            if self.isg == 0:
                self.gold = 0
            if self.iss == 0:
                self.silver = 0

    def handle_data(self, data):
        if self.flagg == 1:
            self.gold = data.strip()
            self.flagg = 0

        if self.flags == 1:
            self.silver = data.strip()
            self.flags = 0

        if self.flagb == 1:
            self.bons = data.strip()
            self.flagb = 0

class V2HTMLParserL(HTMLParser):
    """ check login status """
    def __init__(self):
        self.wstatus = 0
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for _, val in attrs:
                if 'problem' in val:
                    self.wstatus = 1
                    return
