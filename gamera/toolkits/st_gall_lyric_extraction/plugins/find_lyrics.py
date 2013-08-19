from gamera.plugin import *
# Implementation in Pure Python because I'm having segfaulting problems with C++

#import _count_under_func

import sys
#from numpy import NaN, Inf, arange, isscalar, array, argmax
 
#def peakdet(v, delta, minimum_y_threshold = 500, minimum_x_threshold = 50, x = None):
#    """
#    Converted from MATLAB script at http://billauer.co.il/peakdet.html
#    
#    Returns two arrays
#    
#    function [maxtab, mintab]=peakdet(v, delta, x)
#    %        [MAXTAB, MINTAB] = PEAKDET(V, DELTA) finds the local
#    %        maxima and minima ("peaks") in the vector V.
#    %        MAXTAB and MINTAB consists of two columns. Column 1
#    %        contains indices in V, and column 2 the found values.
#    %      
#    %        With [MAXTAB, MINTAB] = PEAKDET(V, DELTA, X) the indices
#    %        in MAXTAB and MINTAB are replaced with the corresponding
#    %        X-values.
#    %
#    %        A point is considered a maximum peak if it has the maximal
#    %        value, and was preceded (to the left) by a value lower by
#    %        DELTA.
#    %        MINIMUM_Y_THRESHOLD is the threshold for minimum maximum
#    %           values
#    %        MINIMUM_X_THRESHOLD: minimum horizontal difference between 2
#    %           maximum candidates
#    """
#
#    maxtab = []
#    mintab = []
#       
#    if x is None:
#        x = arange(len(v))
#    
#    v = array(v)
#    
#    if len(v) != len(x):
#        sys.exit('Input vectors v and x must have same length')
#    
#    if not isscalar(delta):
#        sys.exit('Input argument delta must be a scalar')
#    
#    if delta <= 0:
#        sys.exit('Input argument delta must be positive')
#    
#    mn, mx = Inf, -Inf
#    mnpos, mxpos = NaN, NaN
#    
#    lookformax = True
#    
#    for i in arange(len(v)):
#        this = v[i]
#        if this > mx:
#            mx = this
#            mxpos = x[i]
#        if this < mn:
#            mn = this
#            mnpos = x[i]
#        
#        if lookformax:
#            if this < mx-delta and this >= minimum_y_threshold:
#        
#                maxtab.append((mxpos, mx))
#                mn = this
#                mnpos = x[i]
#                lookformax = False
#        else:
#            if this > mn+delta:
#                mintab.append((mnpos, mn))
#                mx = this
#                mxpos = x[i]
#                lookformax = True
# 
#    # check for close max candidates, choose only one
#    for i in range(len(maxtab)-1, 0, -1):
#        if maxtab[i][0]-maxtab[i-1][0] < minimum_x_threshold: # minimum x threshold
#            if maxtab[i][1] >= maxtab[i-1][1]:
#                del maxtab[i-1]
#            else:
#                del maxtab[i]
#
#    return array(maxtab), array(mintab)

class count_black_under_line(PluginFunction):
  """
  Returns the number of pixels beneath a given line that are black.
  The arguments 'slope' and 'y_intercept' correspond to the m and b in the
  equation of a line, y = m * x + b, respectively. I don't know if this works
  properly because I've had it count white pixels as black ones...
  """
  self_type = ImageType([ONEBIT])
  return_type = Int("num_black_pixels")
  args = Args([Real("slope"), Real("y_intercept")])
  doc_examples = [(ONEBIT,)]

class show_the_black_bug(PluginFunction):
  """
  If a pixel is black print its coordinates, otherwise don't.
  """
  self_type = ImageType([ONEBIT])
  return_type = None
  args = Args([Int("x_range"), Int("y_range")])
  doc_examples = [(ONEBIT,)]

class show_the_black_bug_b(PluginFunction):
  """
  If a pixel is black store its coordinates in a vector.
  """
  self_type = ImageType([ONEBIT])
  return_type = IntVector("black_values")
  args = Args([Int("x_range"), Int("y_range")])
  doc_examples = [(ONEBIT,)]

#class count_colour_under_line(PluginFunction):
#  """
#  Returns the number of pixels beneath a given line that are the given colour.
#  The arguments 'slope' and 'y_intercept' correspond to the m and b in the
#  equation of a line, y = m * x + b, respectively.
#  """
#  self_type = ImageType(ALL)
#  return_type = Int("num_coloured_pixels")
#  args = Args([Real("slope"), Real("y_intercept"), Pixel("pixel_value", \
#    default=NoneDefault)])
#  doc_examples = [(ONEBIT,)]

class count_black_under_line_points(PluginFunction):
  """
  Returns the number of pixels beneath a given line that are the given colour.
  The arguments x0, y0 are the start coordinates of the line and the arguments
  x1, y1 are the end coordinates of the line.
  """
  self_type = ImageType([ONEBIT])
  return_type = Int("num_black_pixels")
  args = Args([Real("x0"), Real("y0"), Real("x1"), Real("y1")])
  doc_examples = [(ONEBIT,)]

class remove_ccs_intersected_by_lines(PluginFunction):
  """
  Accept a list of ccs and a list of (slope,y-intercept) tuples and return a
  list of ccs that weren't crossed by any of the line functions in lines.
  """
  self_type = None
  args = Args([ImageList('list_of_connected_components'), \
    Class("list_m_b_pairs")])
  return_type = ImageList('list_of_remaining_connected_components')

#class hl_ccs_under_lines(PluginFunction):
#  """
#  Works on a binarised image. Returns an rgb image with the ccs that the lines
#  crossed colored a given color.
#  """
#  self_type = ImageType([ONEBIT])
#  args = Args([Class("list_m_b_pairs"), Pixel("PixelValue")])
#  return_type = ImageType([RGB])

class Count_under_funcModule(PluginModule):
  category = "Analysis"
  cpp_headers = ["find_lyrics.hpp"]
#  functions = [count_black_under_line, count_black_under_line_points, \
#      colour_image_using_ccs]
  functions = [count_black_under_line, count_black_under_line_points, \
      show_the_black_bug, show_the_black_bug_b, remove_ccs_intersected_by_lines]
  author = "Nicholas Esterer"
  url = "nicholas.esterer@gmail.com"

module = Count_under_funcModule()
