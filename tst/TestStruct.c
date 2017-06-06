
#include <stdlib.h>
#include <inttypes.h>
#include "TestStruct.h"
void lmcp_pack_TestStruct(uint8_t* buf, TestStruct* i) {
    uint8_t* outb = buf;
    lmcp_pack_uint16_t(outb, i->tstfield_ai.length);
    outb += 2;
    for (uint32_t index = 0; index < i->tstfield_ai.length; index++) {
        lmcp_pack_uint32_t(outb, i->tstfield[index]);
        outb += sizeof(uint32_t);
    }
}
void lmcp_unpack_TestStruct(uint8_t* buf, TestStruct** outp) {
    *outp = malloc(sizeof(TestStruct));
    TestStruct* out = *outp;
    uint8_t* inb = buf;
    uint32_t tmp;
    uint16_t tmp16;
    uint8_t isnull;
    uint32_t objtype;
    uint32_t objseries;
    inb += lmcp_unpack_uint16_t(inb, &tmp16);
    tmp = tmp16;
    (out)->tstfield = malloc(sizeof(uint32_t) * tmp);
    out->tstfield_ai.length = tmp;
    for (uint32_t index = 0; index < out->tstfield_ai.length; index++) {
        inb += lmcp_unpack_uint32_t(inb, &out->tstfield[index]);
    }
}
uint32_t lmcp_packsize_TestStruct (TestStruct* i) {
    uint32_t out = 0;
    out += 2;
    for (uint32_t index = 0; index < i->tstfield_ai.length; index++) {
        out += sizeof(uint32_t);
    }
    return out;
}
void lmcp_init_TestStruct (TestStruct* i) {
    (*i) = (const TestStruct) {
        0
    };
    ((lmcp_object*)i) -> type = 1;
}
