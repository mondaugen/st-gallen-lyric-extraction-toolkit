St. Gallen Lyric Extraction

Algorithms for finding lines that cross over the lyrics in staffless music. The
lyrics may have a skewed trajectory. After estimating these lines, an algorithm
exists for removing connected components found beneath a given line.

By Nicholas Esterer

nicholas [dot] esterer [at] gmail [dot] com

Peak detection algorithm contributed by Gabriel Vigliensoni

gabriel [at] vigliensoni [dot] com

Usage:

See tests/ for some example workflows.

Installing:

Navigate to the root of the source tree (at the same level as this readme file).

Set the CFLAGS environment variable to something like this:

export CFLAGS="-Wall -O0 -g -I/path/to/the/gamera/build/include/directory"

(see clean-alt-build-script-plugin-testing-env-26-8-13.bash for an idea of what
this path looks like)

you should then be able to install by doing:

./clean-alt-build-script.bash

See the Gamera documentation related to writing toolkits for more information on
how to install toolkits.

http://gamera.sourceforge.net/doc/html/writing_toolkits.html#building-and-installing-a-toolkit

The python documentation on Installing Python Modules can be helpful, too.

http://docs.python.org/2.7/install/index.html

See doc/st-gall-lyric-extraction-diagram-1.pdf for a diagram explaining the
algorithm.

Look in logs/ to see some examples of parameters that users of the algorithm
have found useful.
