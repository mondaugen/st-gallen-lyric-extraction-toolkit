#!/bin/bash
sudo rm -r /Users/nickesterer/Documents/development/gamera_3.3.3_env/\
lib/python2.7/site-packages/gamera/toolkits/st_gall_lyric_extraction
sudo rm -r ./build
sudo rm ./gamera/toolkits/st_gall_lyric_extraction/plugins/_find_lyrics.so
export CFLAGS="-Wall -O0 -g -I/Users/nickesterer/Documents/build/Gamera/include";  sudo python \
setup.py build &&  sudo python setup.py install &&  sudo python setup.py install_scripts;
exit 0
