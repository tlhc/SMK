#!/usr/bin/env python
# coding:utf-8
# author TL

""" AppExp """

class AppExp(Exception):
    """ App Exp """
    def __init__(self, value):
        self.expstr = value
        Exception.__init__(self)
    def __str__(self):
        return repr(self.expstr)

