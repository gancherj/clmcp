#include "common/struct_defines.h"
#include "Struct1.h"
#include "Struct2.h"
uint32_t lmcp_packsize(lmcp_object* o) {
    switch (o->type) {
    case 1:
        return 15 + lmcp_packsize_Struct1((Struct1*)o);

        break;
    case 2:
        return 15 + lmcp_packsize_Struct2((Struct2*)o);

        break;
    default:
        return 0;
    }
}
void lmcp_free(lmcp_object *o) {
    switch (o->type) {
    case 1:
        lmcp_free_Struct1((Struct1*)o);

        break;
    case 2:
        lmcp_free_Struct2((Struct2*)o);

        break;
    default:
        return;
    }
}
uint32_t lmcp_pack(uint8_t* buf, lmcp_object* o) {
    uint8_t* outb = buf;
    switch (o->type) {
    case 1:
        if (o==NULL) {
            outb += lmcp_pack_uint8_t(outb, 0);
            return 1;
        } else {
            outb += lmcp_pack_uint8_t(outb, 1);
            memcpy(outb, "MYTEST  ", 8);
            outb += 8;
            outb += lmcp_pack_uint32_t(outb, 1);
            outb += lmcp_pack_uint16_t(outb, 1);
        }
        return 15 + lmcp_pack_Struct1(outb, (Struct1*)o);

        break;
    case 2:
        if (o==NULL) {
            outb += lmcp_pack_uint8_t(outb, 0);
            return 1;
        } else {
            outb += lmcp_pack_uint8_t(outb, 1);
            memcpy(outb, "MYTEST  ", 8);
            outb += 8;
            outb += lmcp_pack_uint32_t(outb, 2);
            outb += lmcp_pack_uint16_t(outb, 1);
        }
        return 15 + lmcp_pack_Struct2(outb, (Struct2*)o);

        break;
    default:
        return 0;
    }
}
size_t lmcp_unpack(uint8_t* buf, lmcp_object **o) {
    uint8_t* inb = buf;
    uint32_t tmp;
    uint16_t tmp16;
    uint8_t isnull;
    uint32_t objtype;
    uint16_t objseries;
    char seriesname[8];
    inb += lmcp_unpack_uint8_t(inb, &isnull);
    if (isnull == 0) {
        return 1;
    } else {
        memcpy(seriesname, inb, 8);
        inb += 8;
        inb += lmcp_unpack_uint32_t(inb, &objtype);
        inb += lmcp_unpack_uint16_t(inb, &objseries);
        switch (objtype) {
        case 1:
            lmcp_init_Struct1((Struct1**)o);
            return 15 + lmcp_unpack_Struct1(inb, (Struct1*)(*o));

            break;
        case 2:
            lmcp_init_Struct2((Struct2**)o);
            return 15 + lmcp_unpack_Struct2(inb, (Struct2*)(*o));

            break;
        default:
            return 15;
        }
    }
}
