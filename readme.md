St. Gallen Lyric Extraction

Algorithms for finding lines that cross over the lyrics in staffless music. The
lyrics may have a skewed trajectory. After estimating these lines, an algorithm
exists for removing connected components found beneath a given line.

See /tests for some example workflows.

By Nicholas Esterer
nicholas [dot] esterer [at] gmail [dot] com

Peak detection algorithm contributed by Gabriel Vigliensoni
gabriel [at] vigliensoni [dot] com

Installing:

See clean-alt-build-script.bash. You will have to change the CFLAGS export to
something like this:

export CFLAGS="-Wall -O0 -g -I/path/to/the/gamera/build/include/directory"

(see clean-alt-build-script.bash for an idea of what this path looks like)
I suggest copying clean-alt-build-script.bash to something like
my-clean-alt-build-script.bash and then making the change.
Then do:

chmod u+x ./my-clean-alt-build-script.bash

you should then be able to install by doing:

./my-clean-alt-build-script.bash

See the Gamera documentation related to writing toolkits for more information on
how to install toolkits.

http://gamera.sourceforge.net/doc/html/writing_toolkits.html#building-and-installing-a-toolkit

The python documentation on Installing Python Modules can be helpful, too.

http://docs.python.org/2.7/install/index.html
