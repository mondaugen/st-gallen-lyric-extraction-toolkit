#!/bin/bash
CFLAGS=${CFLAGS:?"Need to set CFLAGS with the path to Gamera/include (and set \
other flags if you want to)"}
sudo pip uninstall st_gall_lyric_extraction
sudo rm -r ./build
sudo rm ./gamera/toolkits/st_gall_lyric_extraction/plugins/_find_lyrics.so
sudo python \
setup.py build &&  sudo python setup.py install &&  sudo python setup.py install_scripts;
exit 0
