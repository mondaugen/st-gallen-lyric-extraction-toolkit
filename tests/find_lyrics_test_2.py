from gamera.core import *
from gamera.toolkits.st_gall_lyric_extraction import find_lyrics
import time
import sys
import os

# arg 1 is source file
# arg 2 is destination folder
# arg 3 is the minimum y threshold
# arg 4 is the number of searches to do at each height division
# arg 5-6 are the negative and positive height bounds around which to search
# example: ./source_file ./dest_dir 10 4 10 10
# will do 10 * 4 = 40 searches, each line starting from h_i = height/10 * (i + 0.5) for i
# in [0,10) and searching to end_h_j = (h_i) - 10 + (10 + 10)* (j + 0.5) / 4 for
# j in [0,4)

init_gamera()

img = load_image(sys.argv[1]).to_rgb()

onebit = img.to_onebit()

minimum_y_threshold = int(sys.argv[3])
num_searches        = int(sys.argv[4])
negative_bound      = int(sys.argv[5])
postive_bound       = int(sys.argv[6])

noninvimg = onebit.image_copy()
ccs = noninvimg.cc_analysis()
#onebit.invert()

lines = onebit.find_blackest_lines( minimum_y_threshold, \
                                    num_searches, \
                                    negative_bound, \
                                    postive_bound )

print "Blackest lines:", lines

mb_lines = [find_lyrics.slope_intercept_from_points(p0,p1) for p0, p1 in lines]


print "Number of ccs before", len(ccs)

func = find_lyrics.remove_ccs_intersected_by_lines

newccs = func(ccs, mb_lines, 0)

print "Number of newccs after", len(newccs)

for m, b in mb_lines:
  print m, b
  print onebit.lr.x, m * onebit.lr.x + b
  img.draw_line(FloatPoint(onebit.ul.x, onebit.ul.x * m + b),
                FloatPoint(onebit.lr.x, m * onebit.lr.x + b), 
                RGBPixel(0,0,0))

for cc in set(ccs) - set(newccs):
  img.highlight(cc, RGBPixel(255,0,0))

pathprepend = sys.argv[2]

imagedir = pathprepend + "/blackest_line_" + time.strftime("%y-%m-%d")

try:
  os.mkdir(imagedir)
except OSError as e:
  print "Directory already exists, but that's cool."

imagepath = imagedir + "/" + time.strftime("%H_%M_%S")\
    +"-"+os.path.basename(sys.argv[1])

img.save_PNG(imagepath)
