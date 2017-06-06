#include "TestStruct.h"
#include <inttypes.h>
uint32_t* f(uint32_t* i, uint32_t size) {
    TestStruct ti;
    lmcp_init_TestStruct(&ti);

    ti.tstfield = malloc(sizeof(uint32_t) * size);
    ti.tstfield_ai.length = size;
    memcpy(ti.tstfield, i, sizeof(uint32_t) * size);


    uint8_t* buf = malloc(lmcp_packsize_TestStruct(&ti));
    lmcp_pack_TestStruct(buf, &ti);

    TestStruct *to;

    lmcp_unpack_TestStruct(buf, &to);


    return to->tstfield;
}

