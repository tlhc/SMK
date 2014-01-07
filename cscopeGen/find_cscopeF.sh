#!/bin/bash - 
#===============================================================================
#
#          FILE: find_cscopeF.sh
# 
#         USAGE: ./find_cscopeF.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: tongl (), 
#  ORGANIZATION: 
#       CREATED: 2014年01月07日 11时23分40秒 CST
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error

rm ./cscope.files
if [ $? -eq 0 ] ; then
    echo "rm success"
else 
    echo "no pre cscope.files!! will Gen one for you!!!"
fi

find ./ -iname "*.c" -o -iname "*.h" -o -iname "*.cc" -o -iname "*.hh" -o -iname "*.hpp" -o -iname "*.cpp" -o -iname "*.java" -o -iname "*.cs" -o -iname "*.js" -o -iname "*.py" -o -iname "*.rb" -o -iname "*.sh" -o -iname "*.lua" > cscope.files

if [ $? -eq 0 ] ; then
    echo "find cscope.files  success"
else 
    exit
fi

echo "start Gen cscope database....."

cscope -bq -i ./cscope.files

echo "Gen success!! enjoryyyyyyyyy!"
