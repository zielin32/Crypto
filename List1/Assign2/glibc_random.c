#include <stdlib.h>
#include "glibc_random.h"

unsigned long call_glibc_random()
{
    return rand();
}