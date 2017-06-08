
#include <stdlib.h>
#include <inttypes.h>
#include "common/struct_defines.h"
#include "common/conv.h"
#include "Struct1.h"
size_t lmcp_packsize_Struct1 (Struct1* i) {
    size_t out = 0;
    out += sizeof(uint16_t);
    return out;
}
size_t lmcp_unpack_Struct1(uint8_t* buf, Struct1* outp) {
    Struct1* out = outp;
    uint8_t* inb = buf;
    uint32_t tmp;
    uint16_t tmp16;
    uint8_t isnull;
    uint32_t objtype;
    uint16_t objseries;
    char seriesname[8];
    inb += lmcp_unpack_uint16_t(inb, &(out->field1));
    return (inb - buf);
}
size_t lmcp_pack_Struct1(uint8_t* buf, Struct1* i) {
    if (i == NULL) return 0;
    uint8_t* outb = buf;
    outb += lmcp_pack_uint16_t(outb, i->field1);
    return (outb - buf);
}
void lmcp_init_Struct1 (Struct1** i) {
    (*i) = malloc(sizeof(Struct1*));
    *(*i) = (const Struct1) {
        0
    };
    ((lmcp_object*)(*i)) -> type = 1;
}
void lmcp_free_Struct1(Struct1* out) {
    if (out == NULL)
        return;
    free(out);
}
