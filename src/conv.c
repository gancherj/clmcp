#include "conv.h"

uint16_t i16_htonl (uint16_t in) {
    uint8_t* s = (uint8_t*)&in;
    return
    ((uint16_t)s[0] << 8)
    | ((uint16_t)s[1] << 0);
}

uint32_t i32_htonl (uint32_t in) {
    uint8_t* s = (uint8_t*)&in;
    return
    ((uint32_t)s[0] << 24)
    |((uint32_t)s[1] << 16)
    |((uint32_t)s[2] << 8)
    |((uint32_t)s[3] << 0);
}

uint64_t i64_htonl (uint64_t in) {
    uint8_t* s = (uint8_t*)&in;
    return
    ((uint64_t)s[0] << 56)
    |((uint64_t)s[1] << 48)
    |((uint64_t)s[2] << 40)
    |((uint64_t)s[3] << 32)
    |((uint64_t)s[4] << 24)
    |((uint64_t)s[5] << 16)
    |((uint64_t)s[6] << 8)
    |((uint64_t)s[7] << 0);
}

