
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

// TODO: fix these so I can prove in saw that they are mutual inverses on all inputs.


uint64_t i64_unpack_big_endian (const uint8_t* s) {
    return
        (uint64_t)s[0] << 56
        |(uint64_t)s[1] << 56
        |(uint64_t)s[2] << 40
        |(uint64_t)s[3] << 32
        |(uint64_t)s[4] << 24
        |(uint64_t)s[5] << 16
        |(uint64_t)s[6] << 8
        |(uint64_t)s[7] << 0;
}

void i64_pack_big_endian (uint8_t* s, uint64_t i) {
    s[0] = (uint8_t) (i >> 56);
    s[1] = (uint8_t) (i >> 48);
    s[2] = (uint8_t) (i >> 40);
    s[3] = (uint8_t) (i >> 32);
    s[4] = (uint8_t) (i >> 24);
    s[5] = (uint8_t) (i >> 16);
    s[6] = (uint8_t) (i >> 8);
    s[7] = (uint8_t) (i >> 0);
}

uint64_t i64_s2b(uint64_t in) {
    return i64_unpack_big_endian((uint8_t*)&in);
}

uint64_t i64_b2s(uint64_t in) {
    uint8_t buf[8];
    i64_pack_big_endian(buf, in);
    return *(uint64_t*)buf;
}

int main() {
    uint64_t j = 9827398472374;
    printf("%llu", i64_b2s(j));
}
