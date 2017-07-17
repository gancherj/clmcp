
#include <stdlib.h>
#include <inttypes.h>
#include "common/struct_defines.h"
#include "common/conv.h"
#include "Struct2.h"
#include "Struct1.h"
size_t lmcp_packsize_Struct2 (Struct2* i) {
    size_t out = 0;
    out += lmcp_packsize_Struct1(&(i->super));
    out += sizeof(uint16_t);
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
    lmcp_unpack_Struct1(inb, size_remain, &(out->super));
    lmcp_unpack_uint16_t(inb, size_remain, &(out->field2));
}
size_t lmcp_pack_Struct2(uint8_t* buf, Struct2* i) {
    if (i == NULL) return 0;
    uint8_t* outb = buf;
    outb += lmcp_pack_Struct1(outb, &(i->super));
    outb += lmcp_pack_uint16_t(outb, i->field2);
    return (outb - buf);
}
