#!/usr/bin/env python
# coding:utf-8

""" copy src_dir's dir to dest dir """
import os
import sys
import shutil
import getopt

def main():
    """ main """
    source_dir = './'
    dest_dir = ''
    opts, _ = getopt.getopt(sys.argv[1:], 's:d:', ['source=', 'dist='])
    for opt, arg in opts:
        if opt == '-s':
            source_dir = arg
        if opt == '-d':
            dest_dir = arg

    if not os.path.exists(source_dir):
        print 'src dir is not exists'
        return
    if not os.path.isdir(source_dir):
        print 'src is not dir'
        return

    for _dir in [source_dir.rstrip('/') + '/' + item
                 for item in os.listdir(source_dir)]:
        if os.path.isdir(os.path.abspath(_dir)):
            try:
                _tmpdest = dest_dir.rstrip('/') + \
                           '/' + ''.join(_dir.split('/')[-1:])
                shutil.copytree(os.path.abspath(_dir),
                                os.path.abspath(_tmpdest))
                print 'copy.. ' + _dir + ' to ' + _tmpdest
            except OSError as ex:
                print ex

if __name__ == '__main__':
    main()
