
#include <stdlib.h>
#include <inttypes.h>
#include "common/struct_defines.h"
#include "common/conv.h"
#include "TestStruct.h"
size_t lmcp_packsize_TestStruct (TestStruct* i) {
    size_t out = 0;
    out += 2;
    for (uint32_t index = 0; index < i->tstfield_ai.length; index++) {
        out += sizeof(uint32_t);
    }
    return out;
}
size_t lmcp_pack_TestStruct_header(uint8_t* buf, TestStruct* i) {
    uint8_t* outb = buf;
    if (i == NULL) {
        lmcp_pack_uint8_t(outb, 0);
        return 1;
    }
    else {
        outb += lmcp_pack_uint8_t(outb, 1);
        memcpy(outb, "MYTEST  ", 8);
        outb += 8;
        outb += lmcp_pack_uint32_t(outb, 1);
        outb += lmcp_pack_uint16_t(outb, 1);
        return 15;
    }
}
void lmcp_free_TestStruct(TestStruct* out) {
    if (out == NULL)
        return;
    if (out->tstfield != NULL) {
        free(out->tstfield);
    }
    free(out);
}
void lmcp_init_TestStruct (TestStruct** i) {
    if (i == NULL) return;
    (*i) = malloc(sizeof(TestStruct));
    *(*i) = (const TestStruct) {
        0
    };
    ((lmcp_object*)(*i)) -> type = 1;
}
void lmcp_unpack_TestStruct(uint8_t** inb, size_t *size_remain, TestStruct* outp) {
    if (inb == NULL || *inb == NULL) {
        *inb = NULL;
        return;
    }
    if (size_remain == NULL || *size_remain == 0) {
        *inb = NULL;
        return;
    }
    TestStruct* out = outp;
    uint32_t tmp;
    uint16_t tmp16;
    uint8_t isnull;
    uint32_t objtype;
    uint16_t objseries;
    char seriesname[8];
    lmcp_unpack_uint16_t(inb, size_remain, &tmp16);
    tmp = tmp16;
    (out)->tstfield = malloc(sizeof(uint32_t) * tmp);
    if (out->tstfield==0) {
        *inb = NULL;
        return;
    }
    out->tstfield_ai.length = tmp;
    for (uint32_t index = 0; index < out->tstfield_ai.length; index++) {
        lmcp_unpack_uint32_t(inb, size_remain, &out->tstfield[index]);
    }
}
size_t lmcp_pack_TestStruct(uint8_t* buf, TestStruct* i) {
    if (i == NULL) return 0;
    uint8_t* outb = buf;
    outb += lmcp_pack_uint16_t(outb, i->tstfield_ai.length);
    for (uint32_t index = 0; index < i->tstfield_ai.length; index++) {
        outb += lmcp_pack_uint32_t(outb, i->tstfield[index]);
    }
    return (outb - buf);
}
