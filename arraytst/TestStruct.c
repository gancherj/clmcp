
#include <stdlib.h>
#include <inttypes.h>
#include "common/struct_defines.h"
#include "common/conv.h"
#include "TestStruct.h"
size_t lmcp_pack_TestStruct(uint8_t* buf, TestStruct* i) {
    if (i == NULL) return 0;
    uint8_t* outb = buf;
    outb += lmcp_pack_uint16_t(outb, i->tstfield_ai.length);
    for (uint32_t index = 0; index < i->tstfield_ai.length; index++) {
        outb += lmcp_pack_uint32_t(outb, i->tstfield[index]);
    }
    return (outb - buf);
}
size_t lmcp_unpack_TestStruct(uint8_t* buf, TestStruct* outp) {
    TestStruct* out = outp;
    uint8_t* inb = buf;
    uint32_t tmp;
    uint16_t tmp16;
    uint8_t isnull;
    uint32_t objtype;
    uint16_t objseries;
    char seriesname[8];
    inb += lmcp_unpack_uint16_t(inb, &tmp16);
    tmp = tmp16;
    (out)->tstfield = malloc(sizeof(uint32_t*) * tmp);
    out->tstfield_ai.length = tmp;
    for (uint32_t index = 0; index < out->tstfield_ai.length; index++) {
        inb += lmcp_unpack_uint32_t(inb, &out->tstfield[index]);
    }
    return (inb - buf);
}
void lmcp_free_TestStruct(TestStruct* out) {
    if (out == NULL)
        return;
    if (out->tstfield != NULL) {
        free(out->tstfield);
    }
    free(out);
}
size_t lmcp_packsize_TestStruct (TestStruct* i) {
    size_t out = 0;
    out += 2;
    for (uint32_t index = 0; index < i->tstfield_ai.length; index++) {
        out += sizeof(uint32_t);
    }
    return out;
}
void lmcp_init_TestStruct (TestStruct** i) {
    (*i) = malloc(sizeof(TestStruct));
    *(*i) = (const TestStruct) {
        0
    };
    ((lmcp_object*)(*i)) -> type = 1;
}
