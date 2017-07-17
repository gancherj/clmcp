#include "lmcp.h"
#include <stdio.h>

uint32_t f(uint32_t i) {
    TestStruct *ts;
    lmcp_init_TestStruct(&ts);

    ts->tstfield = i;

    size_t size = 15 + lmcp_packsize_TestStruct(ts);
    uint8_t* buf = malloc(size);
    uint8_t* outb = buf; 

    outb += lmcp_pack_TestStruct_header(outb, ts);
    outb += lmcp_pack_TestStruct(outb, ts);

    TestStruct *ts2;
    lmcp_init_TestStruct(&ts2);
    uint8_t* inb = buf + 15;
    size_t size_remain = size;
    lmcp_unpack_TestStruct(&inb, &size_remain, ts2);

    uint32_t out = ts2->tstfield;

    lmcp_free_TestStruct(ts);
    lmcp_free_TestStruct(ts2);
    free(buf);
    return out;
}

int main() {
    printf("%d", f(37));
}
