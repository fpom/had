# Headers as Dependencies

HaD reads the `#include`d headers from a bunch of C files and prints the corresponding compiler options. For instance, if `#include <math.h>` is used, option `-lm` is required, or if `#include <pthread.h>` is used, `-pthread` is required.

To do so, HaD relies on a database maintained by hand, as well as on `pkg-config`. It currently supports only GCC and Clang on Linux.

You can help a lot by enriching files `hadlib/*.cfg`.
