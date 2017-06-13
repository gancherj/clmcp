
#include <stdlib.h>
#include <inttypes.h>
#include "common/struct_defines.h"
#include "common/conv.h"
#include "Struct2.h"
#include "Struct1.h"
size_t lmcp_packsize_Struct2 (Struct2* i) {
    size_t out = 0;
    out += 2;
    for (uint32_t index = 0; index < i->field2_ai.length; index++) {
        out += 15 + lmcp_packsize_Struct1(i->field2[index]);
    }
    return out;
}
size_t lmcp_pack_Struct2_header(uint8_t* buf, Struct2* i) {
    uint8_t* outb = buf;
    if (i == NULL) {
        lmcp_pack_uint8_t(outb, 0);
        return 1;
    }
    else {
        outb += lmcp_pack_uint8_t(outb, 1);
        memcpy(outb, "MYTEST  ", 8);
        outb += 8;
        outb += lmcp_pack_uint32_t(outb, 2);
        outb += lmcp_pack_uint16_t(outb, 1);
        return 15;
    }
}
void lmcp_free_Struct2(Struct2* out) {
    if (out == NULL)
        return;
    if (out->field2 != NULL) {
        for (uint32_t index = 0; index < out->field2_ai.length; index++) {
            if (out->field2[index] != NULL) {
                lmcp_free_Struct1(out->field2[index]);
            }
        }
        free(out->field2);
    }
    free(out);
}
void lmcp_init_Struct2 (Struct2** i) {
    if (i == NULL) return;
    (*i) = malloc(sizeof(Struct2));
    *(*i) = (const Struct2) {
        0
    };
    ((lmcp_object*)(*i)) -> type = 2;
}
void lmcp_unpack_Struct2(uint8_t** inb, size_t *size_remain, Struct2* outp) {
    if (inb == NULL || *inb == NULL) {
        *inb = NULL;
        return;
    }
    if (size_remain == NULL || *size_remain == 0) {
        *inb = NULL;
        return;
    }
    Struct2* out = outp;
    uint32_t tmp;
    uint16_t tmp16;
    uint8_t isnull;
    uint32_t objtype;
    uint16_t objseries;
    char seriesname[8];
    lmcp_unpack_uint16_t(inb, size_remain, &tmp16);
    tmp = tmp16;
    (out)->field2 = malloc(sizeof(Struct1*) * tmp);
    if (out->field2==0) {
        *inb = NULL;
        return;
    }
    out->field2_ai.length = tmp;
    for (uint32_t index = 0; index < out->field2_ai.length; index++) {
        lmcp_unpack_uint8_t(inb, size_remain, &isnull);
        if (isnull == 0 && inb != NULL) {
            out->field2[index] = NULL;
        } else if (inb != NULL) {
            lmcp_unpack_8byte(inb, size_remain, seriesname);
            lmcp_unpack_uint32_t(inb, size_remain, &objtype);
            lmcp_unpack_uint16_t(inb, size_remain, &objseries);
            lmcp_init_Struct1(&(out->field2[index]));
            lmcp_unpack_Struct1(inb, size_remain, (out->field2[index]));
        }
    }
}
size_t lmcp_pack_Struct2(uint8_t* buf, Struct2* i) {
    if (i == NULL) return 0;
    uint8_t* outb = buf;
    outb += lmcp_pack_uint16_t(outb, i->field2_ai.length);
    for (uint32_t index = 0; index < i->field2_ai.length; index++) {
        if (i->field2[index]==NULL) {
            outb += lmcp_pack_uint8_t(outb, 0);
        } else {
            outb += lmcp_pack_uint8_t(outb, 1);
            memcpy(outb, "MYTEST  ", 8);
            outb += 8;
            outb += lmcp_pack_uint32_t(outb, 1);
            outb += lmcp_pack_uint16_t(outb, 1);
            outb += lmcp_pack_Struct1(outb, i->field2[index]);
        }
    }
    return (outb - buf);
}
