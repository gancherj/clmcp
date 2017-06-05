#include "util.h"
#include <stdint.h>

uint16_t stlen(const char* c) {
    uint16_t i = 0;
    while (c[i] != '\0')
        i++;
    return i;
}
