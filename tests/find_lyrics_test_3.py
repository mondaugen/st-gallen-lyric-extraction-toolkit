from gamera.core import *
from gamera.toolkits.st_gall_lyric_extraction import find_lyrics
import sys

init_gamera()

img = load_image(sys.argv[1])
onebit = img.to_onebit()

print onebit.count_black_under_line_points(1,1,1,1)
