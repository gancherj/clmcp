#define CHECK_MEM
#include <inttypes.h>
#include <stdio.h>
#include "lmcp.h"



uint32_t serial(uint32_t i, uint8_t* buf, size_t size) {
    TestStruct* t;
    lmcp_init_TestStruct(&t);
    t->tstfield = i;

    lmcp_pack_TestStruct(buf, t);
    lmcp_free_TestStruct(t);

    TestStruct* t2;
    lmcp_init_TestStruct(&t2);
    uint8_t* inb = buf;
    lmcp_unpack_TestStruct(&inb, &size, t2);
    return t2->tstfield;
}

int main() {}
