#include <stdlib.h>
#include "glibc_random.h"

void initialize()
{
    static unsigned int seed = 1;
    static char state[8];

    initstate(seed, state, sizeof(state));
}

long int call_glibc_random()
{
    long r = rand();
    return r;
}