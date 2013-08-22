#ifndef FIND_LYRICS_HPP
#define FIND_LYRICS_HPP 

#include <stdio.h> 
#include "gamera.hpp"
//#include "plugins/draw.hpp"
//#include "plugins/segmentation.hpp"
#include <cstdio> 
#include <vector> 
#include <algorithm> 
#include <iostream> 

using namespace Gamera;

/*
 * An abstract class that allows the creation of arbitrary rational functions.
 */

class RationalFunction {
  public:
    virtual double operator()(double x) = 0;
};

/* 
 * Create a class that can be called like a function, giving the result of the
 * equation y = m * x + b
 */
class LineSegment : public RationalFunction {
  public:
    double slope;
    double yintercept;
    double operator()(double x) {
      /* y = m*x + b */
      return this->slope * x + this->yintercept; 
    };
    LineSegment(double slope, double yintercept) {
      init(slope, yintercept);
    };
    LineSegment(double x0, double y0, double x1, double y1) {
      init((y1 - y0) / (x1 - x0), y0 - x0 * (y1 - y0) / (x1 - x0));
    }
  private:
    void init(double slope, double yintercept) {
      this->slope = slope;
      this->yintercept = yintercept;
    };
};

/*
 * A class that can be called like a function on a connected component,
 * returning true if the function goes through the cc and false if it doesn't.
 */
class CCContainsFunction {
  public:
    RationalFunction *func;
    bool operator()(Cc *cc) {
      static int how_many_calls = 0;
//      std::cout << "Do you get called?" << std::endl;
      std::cout << how_many_calls++
        << ": Corner x's: " << cc->ul_x() << " " << cc->lr_x() << std::endl;
      for (int x = cc->ul_x(); x <= cc->lr_x(); ++x) {
        int y = (int)(*func)(x);
//        std::cout << "Current x,y: " << x << " " << y << std::endl;
//        std::cout << "Output of function y'all: " << y << std::endl;
        if ((y >= cc->ul_y()) && (y <= cc->lr_y())) {
          if (is_black(cc->get(Point(x - cc->ul_x(), y - cc->ul_y())))) {
            return true;
          }
        }
      }
      return false;
    };
    bool operator()(Image *img) {
      Cc *cc = static_cast<Cc*>(img);
      return (*this)(cc);
    };
    CCContainsFunction(RationalFunction *func) {
      this->func = func;
    };
};

//ImageList *
void
remove_ccs_intersected_by_func(ImageList *ccs, RationalFunction &func)
{
  CCContainsFunction ccContainsFunc(&func);
  ImageList result = ImageList();
  ImageList::iterator ccs_it;
  for (ccs_it = ccs->begin(); ccs_it != ccs->end(); ++ccs_it) {
    Cc *cc = static_cast<Cc*>(*ccs_it);
    if (!ccContainsFunc(cc))
      result.push_back(cc);
  }
//  delete ccs;
  *ccs = result;
//  delete result;
//  ccs->remove_if(ccContainsFunc);
}

ImageList*
remove_ccs_intersected_by_lines(std::vector< std::pair<Image*, int> > ccs, PyObject *list_m_b_pairs)
{
  ImageList *result = new ImageList;
  std::vector< std::pair<Image*, int> >::iterator it;
  for (it = ccs.begin(); it != ccs.end(); ++it)
    result->push_back(it->first);

  std::cout << "Length according to C++: " << result->size() << std::endl;
  PyObject *seq, *tup;
  Py_ssize_t i, len;

  seq = PySequence_Fast(list_m_b_pairs, "expected a sequence");
  len = PySequence_Length(seq);

  for (i = 0; i < len; ++i) {
    PyObject *mobj, *bobj;
    tup = PySequence_Fast(PySequence_Fast_GET_ITEM(seq, i),
                          "expected a sequence");
    double m, b;
    mobj = PySequence_Fast_GET_ITEM(tup, 0);
    bobj = PySequence_Fast_GET_ITEM(tup, 1);
    if ((!(PyFloat_Check(mobj))) || (!(PyFloat_Check(bobj)))) // << Change to any Numeric type.
      continue; /* Skip over incompatible tuple args */
    m = PyFloat_AS_DOUBLE(mobj);
    b = PyFloat_AS_DOUBLE(bobj);

    LineSegment lineFunc(m, b);
//    ImageList *newresult = remove_ccs_intersected_by_func(result, lineFunc);
    remove_ccs_intersected_by_func(result, lineFunc);
//    delete result;

    Py_DECREF(tup);
  }

  Py_DECREF(seq);

  return result;
}

template<class T>
int
count_black_under_line(const T &img, double m, double b)
{
  unsigned int count = 0;
  size_t i;
  for (i = img.ul_x(); i < img.lr_x(); ++i) {
    if ( is_black( img.get( Point(i, m * ((double)i) + b) ) ) )
      ++count;
  }
  return count;
}

template<class T>
int
count_black_under_line_points(const T &img, double x0, double y0, double x1, double y1)
{
  return count_black_under_line(img, (y1 - y0) / (x1 - x0), y0 - x0 * (y1 - y0) / (x1 - x0));
}

template<class T>
void
show_the_black_bug(const T &img, int x_range, int y_range)
{
  size_t i, j;
  printf("[");
  for (i = 0; i < x_range; ++i) {
    for (j = 0; j < y_range; ++j) {
      OneBitPixel p;
      if (is_black( p = img.get( Point(i,j) ) ))
        printf("(%d, %d, %d), ", i, j, (int)p);
    }
  }
  /*
  for (i = img.ul_x(); i < img.lr_x(); ++i) {
    for (j = img.ul_y(); j < img.lr_y(); ++j) {
      if (is_black( img.get( Point(i,j) ) ))
        printf("(%d, %d), ", i, j);
    }
  }
  */
  printf("]");
}

template<class T>
std::vector<int> *
show_the_black_bug_b(const T &img, int x_range, int y_range)
{
  size_t i, j;
  std::vector<int> *result = new std::vector<int>();
  for (i = 0; i < x_range; ++i) {
    for (j = 0; j < y_range; ++j) {
      OneBitPixel p;
      if (is_black( p = img.get( Point(i,j) ) ))
        result->push_back((int)p);
    }
  }
  return result;
}

#endif /* FIND_LYRICS_HPP */
