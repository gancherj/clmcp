#include <inttypes.h>
#include <stdio.h>
#include "lmcp.h"

uint32_t f(uint32_t i) {
    TestStruct* ts;
    lmcp_init_TestStruct(&ts);
    ts->tstfield = i;


    TestStruct* ts2;
    size_t packsize = lmcp_packsize_TestStruct(ts);
    uint8_t* buf = malloc(packsize);

    lmcp_pack_TestStruct(buf, ts);

    uint8_t* inb = buf;
    lmcp_init_TestStruct(&ts2);
    lmcp_unpack_TestStruct(&inb, &packsize, ts2);
    uint32_t out = ts2->tstfield;

    lmcp_free_TestStruct(ts);
    lmcp_free_TestStruct(ts2);
    free(buf);

    return out;

}


