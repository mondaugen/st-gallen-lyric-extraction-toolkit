"""
Toolkit setup

This file is run on importing anything within this directory.
Its purpose is only to help with the Gamera GUI shell,
and may be omitted if you are not concerned with that.
"""

from gamera import toolkits
from gamera.toolkits.st_gall_lyric_extraction import main
from gamera.toolkits.st_gall_lyric_extraction.plugins import find_lyrics
