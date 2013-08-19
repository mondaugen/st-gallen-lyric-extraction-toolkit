#!/bin/bash
CFLAGS="-Wall -O0 -g -I/Users/nickesterer/Documents/build/Gamera/include/"  python \
setup.py build &&  python setup.py install &&  python setup.py install_scripts;
exit 0
