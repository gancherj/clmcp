
#include <stdlib.h>
#include <inttypes.h>
#include "common/struct_defines.h"
#include "common/conv.h"
#include "Struct2.h"
#include "Struct1.h"
uint32_t lmcp_packsize_Struct2 (Struct2* i) {
    uint32_t out = 0;
    out += 2;
    for (uint32_t index = 0; index < i->field2_ai.length; index++) {
        out += 15 + lmcp_packsize_Struct1(i->field2[index]);
    }
    return out;
}
size_t lmcp_unpack_Struct2(uint8_t* buf, Struct2** outp) {
    *outp = malloc(sizeof(Struct2));
    Struct2* out = *outp;
    uint8_t* inb = buf;
    uint32_t tmp;
    uint16_t tmp16;
    uint8_t isnull;
    uint32_t objtype;
    uint16_t objseries;
    char seriesname[8];
    inb += lmcp_unpack_uint16_t(inb, &tmp16);
    tmp = tmp16;
    (out)->field2 = malloc(sizeof(Struct1) * tmp);
    out->field2_ai.length = tmp;
    for (uint32_t index = 0; index < out->field2_ai.length; index++) {
        inb += lmcp_unpack_uint8_t(inb, &isnull);
        if (isnull == 0) {
            out->field2[index] = NULL;
        } else {
            out->field2[index] = malloc(sizeof(Struct1));
            memcpy(seriesname, inb, 8);
            inb += 8;
            inb += lmcp_unpack_uint32_t(inb, &objtype);
            inb += lmcp_unpack_uint16_t(inb, &objseries);
            inb += lmcp_unpack_Struct1(inb, &(out->field2[index]));
        }
    }
    return (inb - buf);
}
void lmcp_init_Struct2 (Struct2* i) {
    (*i) = (const Struct2) {
        0
    };
    ((lmcp_object*)i) -> type = 2;
}
size_t lmcp_pack_Struct2(uint8_t* buf, Struct2* i) {
    uint8_t* outb = buf;
    outb += lmcp_pack_uint16_t(outb, i->field2_ai.length);
    for (uint32_t index = 0; index < i->field2_ai.length; index++) {
        if (i->field2[index]==NULL) {
            outb += lmcp_pack_uint8_t(outb, 0);
        } else {
            outb += lmcp_pack_uint8_t(outb, 1);
            memcpy(outb, "MYTEST  ", 8);
            outb += 8;
            outb += lmcp_pack_uint32_t(outb, 2);
            outb += lmcp_pack_uint16_t(outb, 1);
            outb += lmcp_pack_Struct1(outb, i->field2[index]);
        }
    }
    return (outb - buf);
}
