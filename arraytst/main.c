#include "lmcp.h"
#include <inttypes.h>
#include <stdio.h>
TestStruct* g(uint32_t* i, uint32_t size) {
    TestStruct *ti;
    lmcp_init_TestStruct(&ti);

    ti->tstfield = malloc(sizeof(uint32_t) * size);
    ti->tstfield_ai.length = size;
    memcpy(ti->tstfield, i, sizeof(uint32_t) * size);


    uint8_t* buf = malloc(lmcp_packsize_TestStruct(ti));
    lmcp_pack_TestStruct(buf, ti);

    TestStruct *to;
    lmcp_init_TestStruct(&to);
    lmcp_unpack_TestStruct(buf, to);

    free(buf);
    lmcp_free_TestStruct(ti);
    return to;
}

uint32_t* f(uint32_t* i, uint32_t size) {
    TestStruct* to = g(i, size);
    uint32_t* arr = malloc(sizeof(uint32_t) * size);
    memcpy(arr, to->tstfield, sizeof(uint32_t) * size);
    lmcp_free((lmcp_object*)to);
    return arr;

}

int main() {
    uint32_t j[5] = {1,2,3,4,5};
    uint32_t* k = f(j, 5);
    for (int i = 0; i < 5; i++)
        printf("%d\n", k[i]);
    free(k);
}


