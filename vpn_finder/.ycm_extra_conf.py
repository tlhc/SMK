# This file is NOT licensed under the GPLv3, which is the license for the rest
# of YouCompleteMe.
#
# Here's the license text for this file:
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org/>

import os
import ycm_core

# These are the compilation flags that will be used in case there's no
# compilation database set (by default, one is not set).
# CHANGE THIS LIST OF FLAGS. YES, THIS IS THE DROID YOU HAVE BEEN LOOKING FOR.
flags = [
'-Wall',
'-Wextra',
'-Werror',
'-Wc++98-compat',
'-Wno-long-long',
'-Wno-variadic-macros',
'-fexceptions',
'-DNDEBUG',
# You 100% do NOT need -DUSE_CLANG_COMPLETER in your flags; only the YCM
# source code needs it.
'-DUSE_CLANG_COMPLETER',
# THIS IS IMPORTANT! Without a "-std=<something>" flag, clang won't know which
# language to use when compiling headers. So it will guess. Badly. So C++
# headers will be compiled as C headers. You don't want that so ALWAYS specify
# a "-std=<something>".
# For a C project, you would set this to something like 'c99' instead of
# 'c++11'.
'-std=c++11',
# ...and the same thing goes for the magic -x option which specifies the
# language that the files to be compiled are written in. This is mostly
# relevant for c++ headers.
# For a C project, you would set this to 'c' instead of 'c++'.
'-x',
'c++',
'-isystem',
'../BoostParts',
'-isystem',
'/usr/include'
'-isystem',
'/usr/local/include',
'-isystem',
'/usr/include/c++/4.6',
'-isystem',
'/usr/include/clang/3.3/include',
'-isystem',
'/usr/include/i386-linux-gnu',

#for QT
#'-DQT_CORE_LIB',
#'-DQT_GUI_LIB',
#'-DQT_NETWORK_LIB',
#'-DQT_QML_LIB',
#'-DQT_QUICK_LIB',
#'-DQT_SQL_LIB',
#'-DQT_WIDGETS_LIB',
#'-DQT_XML_LIB',

#'-I', '/home/mars/Qt5.3.0/5.3/gcc/mkspecs/linux-clang',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/mkspecs/linux-g++',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/mkspecs/linux-g++-32',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/mkspecs/linux-g++-64',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/mkspecs/linux-llvm',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/Enginio',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtBluetooth',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtCLucene',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtConcurrent',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtCore',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtDBus',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtDeclarative',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtDesigner',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtDesignerComponents',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtGui',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtQuick',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtHelp',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtMultimedia',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtNetwork',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtMultimediaQuick_p',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtMultimediaWidgets',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtNfc',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtQml',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtPrintSupport',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtPlatformSupport',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtOpenGL',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtOpenGLExtensions',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtPositioning',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtQuickParticles',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtQuickTest',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtSerialPort',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtSensors',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtQuickWidgets',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtScript',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtScriptTools',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtSql',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtSvg',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtTest',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtUiTools',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtWebKit',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtWebKitWidgets',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtWebSockets',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtWidgets',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtX11Extras',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtXml',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtXmlPatterns',
#'-I', '/home/mars/Qt5.3.0/5.3/gcc/include/QtZlib',
#'-I', '.',

#include for linux
#'-I', '/usr/include',
#'-I', '/usr/include/arpa',
#'-I', '/usr/include/boost',
#'-I', '/usr/include/clang/3.0/include',
#'-I', '/usr/include/clang/Analysis',
#'-I', '/usr/include/clang/Analysis/Analyses',
#'-I', '/usr/include/clang/Analysis/DomainSpecific',
#'-I', '/usr/include/clang/Analysis/FlowSensitive',
#'-I', '/usr/include/clang/Analysis/Support',
#'-I', '/usr/include/clang/Analysis/Visitors',
#'-I', '/usr/include/clang/ARCMigrate',
#'-I', '/usr/include/clang/AST',
#'-I', '/usr/include/clang/Basic',
#'-I', '/usr/include/clang-c',
#'-I', '/usr/include/clang/CodeGen',
#'-I', '/usr/include/clang/Debian',
#'-I', '/usr/include/clang/Driver',
#'-I', '/usr/include/clang/Frontend',
#'-I', '/usr/include/clang/FrontendTool',
#'-I', '/usr/include/clang/Index',
#'-I', '/usr/include/clang/Lex',
#'-I', '/usr/include/clang/Parse',
#'-I', '/usr/include/clang/Rewrite',
#'-I', '/usr/include/clang/Sema',
#'-I', '/usr/include/clang/Serialization',
#'-I', '/usr/include/clang/StaticAnalyzer/Checkers',
#'-I', '/usr/include/clang/StaticAnalyzer/Core',
#'-I', '/usr/include/clang/StaticAnalyzer/Core/BugReporter',
#'-I', '/usr/include/clang/StaticAnalyzer/Core/PathSensitive',
#'-I', '/usr/include/clang/StaticAnalyzer/Frontend',
#'-I', '/usr/include/dbus-1.0/dbus/dbus',
#'-I', '/usr/include/drm',
#'-I', '/usr/include/eXosip2',
#'-I', '/usr/include/gettext',
#'-I', '/usr/include/GL',
#'-I', '/usr/include/GL/internal',
#'-I', '/usr/include/infiniband',
#'-I', '/usr/include/jthread',
#'-I', '/usr/include/layout',
#'-I', '/usr/include/libdrm',
#'-I', '/usr/include/libexslt',
#'-I', '/usr/include/libkms',
#'-I', '/usr/include/libltdl',
#'-I', '/usr/include/libv4l1',
#'-I', '/usr/include/libxml2/libxml',
#'-I', '/usr/include/libxslt',
#'-I', '/usr/include/linux',
#'-I', '/usr/include/llvm-3.3/llvm',
#'-I', '/usr/include/llvm-3.5/llvm',
#'-I', '/usr/include/llvm-c-3.3/llvm-c',
#'-I', '/usr/include/llvm-c-3.5/llvm-c',
#'-I', '/usr/include/lzo',
#'-I', '/usr/include/mm/mm',
#'-I', '/usr/include/mono-2.0/mono/jit',
#'-I', '/usr/include/mono-2.0/mono/metadata',
#'-I', '/usr/include/mono-2.0/mono/metadata/debug',
#'-I', '/usr/include/mono-2.0/mono/metadata/debug-mono',
#'-I', '/usr/include/mono-2.0/mono/metadata/mono',
#'-I', '/usr/include/mono-2.0/mono/metadata/row',
#'-I', '/usr/include/mono-2.0/mono/metadata/sgen',
#'-I', '/usr/include/mono-2.0/mono/utils/mono',
#'-I', '/usr/include/mono-2.0/mono/utils/mono-dl',
#'-I', '/usr/include/mysql',
#'-I', '/usr/include/net',
#'-I', '/usr/include/netash',
#'-I', '/usr/include/netatalk',
#'-I', '/usr/include/netax25',
#'-I', '/usr/include/neteconet',
#'-I', '/usr/include/netinet',
#'-I', '/usr/include/netipx',
#'-I', '/usr/include/netiucv',
#'-I', '/usr/include/netpacket',
#'-I', '/usr/include/net/ppp',
#'-I', '/usr/include/netrom',
#'-I', '/usr/include/netrose',
#'-I', '/usr/include/nfs',
#'-I', '/usr/include/nouveau',
#'-I', '/usr/include/openssl',
#'-I', '/usr/include/openvpn/openvpn',
#'-I', '/usr/include/osip2',
#'-I', '/usr/include/osipparser2',
#'-I', '/usr/include/osipparser2/headers',
#'-I', '/usr/include/pcap',
#'-I', '/usr/include/protocols',
#'-I', '/usr/include/python2.7',
#'-I', '/usr/include/python2.7/Python',
#'-I', '/usr/include/python3.2mu',
#'-I', '/usr/include/qt4/Qt',
#'-I', '/usr/include/qt4/Qt3Support',
#'-I', '/usr/include/qt4/QtCore',
#'-I', '/usr/include/qt4/QtCore/qconfig',
#'-I', '/usr/include/qt4/QtDBus',
#'-I', '/usr/include/qt4/QtDeclarative',
#'-I', '/usr/include/qt4/QtDesigner',
#'-I', '/usr/include/qt4/QtGui',
#'-I', '/usr/include/qt4/QtHelp',
#'-I', '/usr/include/qt4/QtNetwork',
#'-I', '/usr/include/qt4/QtOpenGL',
#'-I', '/usr/include/qt4/Qt/qconfig',
#'-I', '/usr/include/qt4/QtScript',
#'-I', '/usr/include/qt4/QtScriptTools',
#'-I', '/usr/include/qt4/QtSql',
#'-I', '/usr/include/qt4/QtSvg',
#'-I', '/usr/include/qt4/QtTest',
#'-I', '/usr/include/qt4/QtUiTools',
#'-I', '/usr/include/qt4/QtWebKit',
#'-I', '/usr/include/qt4/QtXml',
#'-I', '/usr/include/qt4/QtXmlPatterns',
#'-I', '/usr/include/rdma',
#'-I', '/usr/include/readline',
#'-I', '/usr/include/rpc',
#'-I', '/usr/include/rpcsvc',
#'-I', '/usr/include/ruby-1.9.1',
#'-I', '/usr/include/ruby-1.9.1/i686-linux/ruby',
#'-I', '/usr/include/ruby-1.9.1/ruby',
#'-I', '/usr/include/ruby-1.9.1/ruby/backward',
#'-I', '/usr/include/scsi',
#'-I', '/usr/include/sound',
#'-I', '/usr/include/unicode',
#'-I', '/usr/include/valgrind',
#'-I', '/usr/include/video',
#'-I', '/usr/include/vmware-vix',
#'-I', '/usr/include/X11',
#'-I', '/usr/include/xcb',
#'-I', '/usr/include/xen',
#'-I', '/usr/include/xorg',

# This path will only work on OS X, but extra paths that don't exist are not
# harmful
'/System/Library/Frameworks/Python.framework/Headers',
'-isystem',
'../llvm/include',
'-isystem',
'../llvm/tools/clang/include',
'-I',
'.',
'-I',
'./ClangCompleter',
'-isystem',
'./tests/gmock/gtest',
'-isystem',
'./tests/gmock/gtest/include',
'-isystem',
'./tests/gmock',
'-isystem',
'./tests/gmock/include',
'-isystem',
'/usr/include',
'-isystem',
'/usr/local/include',
'-isystem',
'/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/../lib/c++/v1',
'-isystem',
'/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/include',
]


# Set this to the absolute path to the folder (NOT the file!) containing the
# compile_commands.json file to use that instead of 'flags'. See here for
# more details: http://clang.llvm.org/docs/JSONCompilationDatabase.html
#
# Most projects will NOT need to set this to anything; you can just change the
# 'flags' list of compilation flags. Notice that YCM itself uses that approach.
compilation_database_folder = ''

if os.path.exists( compilation_database_folder ):
  database = ycm_core.CompilationDatabase( compilation_database_folder )
else:
  database = None

SOURCE_EXTENSIONS = [ '.cpp', '.cxx', '.cc', '.c', '.m', '.mm' ]

def DirectoryOfThisScript():
  return os.path.dirname( os.path.abspath( __file__ ) )


def MakeRelativePathsInFlagsAbsolute( flags, working_directory ):
  if not working_directory:
    return list( flags )
  new_flags = []
  make_next_absolute = False
  path_flags = [ '-isystem', '-I', '-iquote', '--sysroot=' ]
  for flag in flags:
    new_flag = flag

    if make_next_absolute:
      make_next_absolute = False
      if not flag.startswith( '/' ):
        new_flag = os.path.join( working_directory, flag )

    for path_flag in path_flags:
      if flag == path_flag:
        make_next_absolute = True
        break

      if flag.startswith( path_flag ):
        path = flag[ len( path_flag ): ]
        new_flag = path_flag + os.path.join( working_directory, path )
        break

    if new_flag:
      new_flags.append( new_flag )
  return new_flags


def IsHeaderFile( filename ):
  extension = os.path.splitext( filename )[ 1 ]
  return extension in [ '.h', '.hxx', '.hpp', '.hh' ]


def GetCompilationInfoForFile( filename ):
  # The compilation_commands.json file generated by CMake does not have entries
  # for header files. So we do our best by asking the db for flags for a
  # corresponding source file, if any. If one exists, the flags for that file
  # should be good enough.
  if IsHeaderFile( filename ):
    basename = os.path.splitext( filename )[ 0 ]
    for extension in SOURCE_EXTENSIONS:
      replacement_file = basename + extension
      if os.path.exists( replacement_file ):
        compilation_info = database.GetCompilationInfoForFile(
          replacement_file )
        if compilation_info.compiler_flags_:
          return compilation_info
    return None
  return database.GetCompilationInfoForFile( filename )


def FlagsForFile( filename, **kwargs ):
  if database:
    # Bear in mind that compilation_info.compiler_flags_ does NOT return a
    # python list, but a "list-like" StringVec object
    compilation_info = GetCompilationInfoForFile( filename )
    if not compilation_info:
      return None

    final_flags = MakeRelativePathsInFlagsAbsolute(
      compilation_info.compiler_flags_,
      compilation_info.compiler_working_dir_ )

    # NOTE: This is just for YouCompleteMe; it's highly likely that your project
    # does NOT need to remove the stdlib flag. DO NOT USE THIS IN YOUR
    # ycm_extra_conf IF YOU'RE NOT 100% SURE YOU NEED IT.
    try:
      final_flags.remove( '-stdlib=libc++' )
    except ValueError:
      pass
  else:
    relative_to = DirectoryOfThisScript()
    final_flags = MakeRelativePathsInFlagsAbsolute( flags, relative_to )

  return {
    'flags': final_flags,
    'do_cache': True
  }
