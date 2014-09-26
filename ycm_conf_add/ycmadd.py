#!/usr/bin/env python
# -*- coding: utf-8 -*-

import commands
import shutil
import os
import cStringIO
import re


def prsfinc(fcontant):

    if fcontant is '':
        print 'wft.prsfinc'
        return

    prefix = "'-I', '"
    suffix = "',"
    retval = ""
    buf = cStringIO.StringIO(fcontant)
    tmp = buf.readline()
    while tmp is not '':
        tmp = tmp.replace('\n', '')
        newstr = (prefix + tmp + suffix)
        retval += newstr + '\n'
        tmp = buf.readline()

    return retval


def prscycm(fcontant, newins):

    if fcontant is '' or newins is '':
        print 'wtf.prcsycm'
        return
    buf = cStringIO.StringIO(fcontant)
    tmp = buf.readline()
    regxp = re.compile(r'^flags')
    regxpend = re.compile(r']$')
    flagc = 0
    newstr = ''
    while tmp is not '':
        tmp = tmp.replace('\n', '')
        if regxp.search(tmp) is not None:
            flagc = 1
        if flagc and regxpend.search(tmp) is not None:
            flagc = 0
            tmp = tmp.replace(']', '')
            tmp += '\n' + '# project inlcudes\n' + '\n'
            tmp += newins
            tmp += ']'

        newstr += tmp
        newstr += '\n'
        tmp = buf.readline()

    return newstr

def main():
    ycm_ext_ffpath = os.path.expanduser('~') + '/.vim/dot_ycm_extra_conf.py'
    dstfname = ".ycm_extra_conf.py"
    cur_path = os.getcwd()

    if cur_path.strip() == '':
        print 'wtf.'
        return

    st, ret = commands.getstatusoutput('find . -iname "*.c" -o -iname "*.h" \
                                       -o -iname "*.cc" -o -iname "*.hh" \
                                       -o -iname "*.cpp" -o -iname "*.hpp"\
                                       | xargs dirname \
                                       | uniq | xargs readlink -m')

    if int(st) != 0:
        print "find err"
        return

    if not os.path.isfile(ycm_ext_ffpath):
        print "file not exist"

    try:
        shutil.copy(ycm_ext_ffpath, cur_path + '/' + dstfname)
    except (IOError, os.error) as why:
        print why
        return

    newins = prsfinc(ret)
    if newins is '':
        print 'wft.process return val'
        return
    try:
        fc = open(dstfname, 'r+')
        ycmfc = fc.read()
        fc.seek(0)
        fc.truncate()
        fc.write(prscycm(ycmfc, newins))
        fc.close()
    except (IOError, os.errno) as why:
        print 'wtf.' + why

    print 'done'


if __name__ == '__main__':
    main()
