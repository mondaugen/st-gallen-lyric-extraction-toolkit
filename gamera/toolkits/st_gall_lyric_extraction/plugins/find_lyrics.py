from gamera.plugin import *
import _find_lyrics
import sys
import os
 
def peakdet(v, delta, minimum_y_threshold = 500, minimum_x_threshold = 50, x = None):
    # For whatever reason, the build fails when importing these at the top of
    # this script
    from numpy import NaN
    from numpy import Inf
    from numpy import arange
    from numpy import isscalar
    from numpy import array
    from numpy import argmax
    """
    Converted from MATLAB script at http://billauer.co.il/peakdet.html
    
    Returns two arrays
    
    function [maxtab, mintab]=peakdet(v, delta, x)
    %        [MAXTAB, MINTAB] = PEAKDET(V, DELTA) finds the local
    %        maxima and minima ("peaks") in the vector V.
    %        MAXTAB and MINTAB consists of two columns. Column 1
    %        contains indices in V, and column 2 the found values.
    %      
    %        With [MAXTAB, MINTAB] = PEAKDET(V, DELTA, X) the indices
    %        in MAXTAB and MINTAB are replaced with the corresponding
    %        X-values.
    %
    %        A point is considered a maximum peak if it has the maximal
    %        value, and was preceded (to the left) by a value lower by
    %        DELTA.
    %        MINIMUM_Y_THRESHOLD is the threshold for minimum maximum
    %           values
    %        MINIMUM_X_THRESHOLD: minimum horizontal difference between 2
    %           maximum candidates
    """

    maxtab = []
    mintab = []
       
    if x is None:
        x = arange(len(v))
    
    v = array(v)
    
    if len(v) != len(x):
        sys.exit('Input vectors v and x must have same length')
    
    if not isscalar(delta):
        sys.exit('Input argument delta must be a scalar')
    
    if delta <= 0:
        sys.exit('Input argument delta must be positive')
    
    mn, mx = Inf, -Inf
    mnpos, mxpos = NaN, NaN
    
    lookformax = True
    
    for i in arange(len(v)):
        this = v[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]
        
        if lookformax:
            if this < mx-delta and this >= minimum_y_threshold:
        
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn+delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True
 
    # check for close max candidates, choose only one
    for i in range(len(maxtab)-1, 0, -1):
        if maxtab[i][0]-maxtab[i-1][0] < minimum_x_threshold: # minimum x threshold
            if maxtab[i][1] >= maxtab[i-1][1]:
                del maxtab[i-1]
            else:
                del maxtab[i]

    return array(maxtab), array(mintab)

class LineSegment:
  """
  Represents a function returning the result of y = m * x + b
  """
  def __init__(self, slope, yintercept):
    self.slope = slope
    self.yintercept = yintercept

  def __call__(self, x):
    return self.slope * x + self.yintercept


class CCContainsFunction:
  """
  A class that can be called like a function and returns true if the function it
  contains goes through a given connected component and false if it doesn't.
  """
  def __init__(self, func):
    self.func = func

  def __call__(self, cc):
#    print "Checking if cc", cc.label, "contains function."
    for x in xrange(cc.ul.x, cc.lr.x + 1):
      y = round(self.func(float(x)))
      if (y >= cc.ul.y) and (y <= cc.lr.y):
#        print "Pixel value at (%d,%d):" % (x, y)
        pixel_value = cc.get((x - cc.ul.x, y - cc.ul.y))
#        print pixel_value,
        # The cc is 'black' when the pixel value gotten is the same as the ccs
        # label
        if pixel_value == cc.label:
#          print
          return True
#    print
    return False

def slope_intercept_from_points(p0, p1):
  """
  Given two different points on a line, return the slope and y-intercept
  representing that line i.e., m and b in the equation y = m * x + b.
  """
  x0, y0 = p0
  x1, y1 = p1
  if (x0 == x1) and (y0 == y1):
    raise ValueError(("The points must be different, instead got: "
        + "x0=%f y0=%f x1=%f y1=%f") % (x0,y0,x1,y1))
  m = float(y1 - y0)/float(x1 - x0)
  b = m * float(x0) + float(y0)
  return (m, b)

def _find_blackest_lines( img, horizontal_projections, minimum_y_threshold,
    num_searches, negative_bound, positive_bound, delta):

  # The horizontal projections of the image
  hp = horizontal_projections

  # Find peaks in the horizontal projection
  maxtab, mintab = peakdet(hp,delta,minimum_y_threshold)

  # The y values of the projection peaks
  peaksy = sorted([m[0] for m in maxtab] + [img.lr.y])

  blackest_lines = []

  # Find connected components of image
  ccs = img.cc_analysis()

  for ys in peaksy:
    # A list of y coordinates with which to create lines is compiled. These
    # y-coordinates are at each division of the distance spanned by the positive
    # bound and negative bound extending out upward and downward from the
    # horizontal projection peak respectively. The number of divisions is given
    # by num_searches.
    y_ends = ([ys - negative_bound + (positive_bound + negative_bound) * (float(i) + 0.5)
              / num_searches for i in xrange(int(num_searches)) ])

    # Filter out y_ends that are above the upper right corner or below the lower
    # left corner.
    y_ends = filter(lambda item: ((item > img.ul.y) and (item < img.lr.y)), y_ends)

    # Lines are made from the points [(y_end[0],img.ul.x),(y_end[-1],img.lr.x)],
    # [(y_end[1],img.ul.x),(y_end[-2],img.lr.x)], ...
    black_counts = ([ img.count_black_under_line_points(img.ul.x, yl,
      img.lr.x, yr) for yl, yr in zip(reversed(y_ends), y_ends) ])

    blackest_idx = black_counts.index(max(black_counts))

    # Line is returned as array of two points [(x0,y0),(x1,y1)]
    # It finds the pair of points making the line that gives the highest
    # black-count
    blackest_lines.append([(img.ul.x, y_ends[ len(y_ends) - blackest_idx - 1 ]),
      (img.lr.x, y_ends[ blackest_idx ])])

  return blackest_lines


class find_blackest_lines(PluginFunction):
  """
  Operates on a binarised image and a list of its horizontal projections. Finds
  local peaks in the horizontal projections of the image. This means it adds up
  the number of times black is seen in a row and stores the value for each row
  in an array. It then finds local peaks in this array. It then draws a bunch of
  lines on the image, all pivoting around the centres of the horizontal
  projections. It discards all but the lines that cross the most black pixels
  and returns the start and end points of these lines, e.g.
  [ [(x00,y00),(x01,y01)], [(x10,y10),(x11,y11)], ... [(xn0,yn0),(xn1,yn1)] ].

  Parameters:

    minimum_y_threshold: the minimum value that may be considered a local peak
    in the horizontal projection.

    num_searches: the number of searches to do around each local peak

    negative_bound: how far below the local peak to start the line search (this
    value is positive! so the value of negative_bound=10 will start searching 10
    pixels below the peak-point (or -10 pixels. To make this even more
    confusing, the negative direction is actually upward when talking about
    images, but you already knew this from reading the Gamera documentation).

    positive_bound: how far above the local peak to start the line search

    delta: see the delta parameter for the peakdet function above
  """
  self_type = ImageType([ONEBIT])
  args = Args([ Class('horizontal_projections', list),
                Int("minimum_y_threshold"), Int("num_searches"),
                Int("negative_bound"), Int("positive_bound"),
                Int("delta") ])
  return_type = Float("area")
  pure_python = True

  @staticmethod
  def __call__(self, horizontal_projections, minimum_y_threshold, num_searches,
      negative_bound, positive_bound, delta=10):
    return _find_blackest_lines(self, horizontal_projections,
        minimum_y_threshold, num_searches, negative_bound, positive_bound,
        delta)


def remove_ccs_intersected_by_func(ccs, func):
  ccContainsFunc = CCContainsFunction(func)
  return [cc for cc in ccs if not ccContainsFunc(cc)]


def remove_ccs_intersected_by_lines(ccs, list_m_b_pairs):
  """
  Accept a list of ccs and a list of (slope,y-intercept) tuples and return a
  list of ccs that weren't crossed by any of the line functions in lines.
  """
  for m, b in list_m_b_pairs:
    ccs = remove_ccs_intersected_by_func(ccs, LineSegment(m,b))
  return ccs


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

class Count_under_funcModule(PluginModule):
  category = "Analysis"
  cpp_headers = ["find_lyrics.hpp"]
#  functions = [count_black_under_line, count_black_under_line_points, \
#      colour_image_using_ccs]
  functions = [count_black_under_line, count_black_under_line_points,
      find_blackest_lines]
  author = "Nicholas Esterer"
  url = "nicholas.esterer@gmail.com"

module = Count_under_funcModule()
