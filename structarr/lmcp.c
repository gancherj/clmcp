#include "common/struct_defines.h"
#include "lmcp.h"
#include "Struct1.h"
#include "Struct2.h"
uint32_t lmcp_msgsize(lmcp_object* o) {
    return 8 + lmcp_packsize(o);
}
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
    if (o == NULL) {
        return;
    }
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
void lmcp_make_msg(uint8_t* buf, lmcp_object* o) {
    buf[0] = 'L';
    buf[1] = 'M';
    buf[2] = 'C';
    buf[3] = 'P';
    lmcp_pack_uint32_t(buf+4, lmcp_packsize(o));
    lmcp_pack(buf + 8, o);
}
void lmcp_process_msg(uint8_t** inb, size_t size, lmcp_object **o) {
    if (size < 8) {
        return;
    }
    if (inb == NULL || *inb == NULL) {
        *o = NULL;
        return;
    }
    if ((*inb)[0] != 'L' || (*inb)[1] != 'M' || (*inb)[2] != 'C' || (*inb)[3] != 'P') {
        return;
    }
    *inb += 4;
    size_t s = 4;
    uint32_t msglen;
    lmcp_unpack_uint32_t(inb, &s, &msglen);
    if (size < (msglen + 8)) {
        *o = NULL;
        *inb = NULL;
        return;
    }
    lmcp_unpack(inb, msglen, o);
}
void lmcp_unpack(uint8_t** inb, size_t size, lmcp_object **o) {
    if (o == NULL) return;
    size_t* size_remain = &size;
    uint32_t tmp;
    uint16_t tmp16;
    int isnull;
    uint32_t objtype;
    uint16_t objseries;
    char seriesname[8];
    isnull = lmcp_unpack_structheader(inb, size_remain, seriesname, &objtype, &objseries);
    if (isnull == 0) {
        *o = NULL;
        return;
    }
    switch (objtype) {
    case 1:
        lmcp_init_Struct1((Struct1**)o);
        lmcp_unpack_Struct1(inb, size_remain, (Struct1*)(*o));

        break;
    case 2:
        lmcp_init_Struct2((Struct2**)o);
        lmcp_unpack_Struct2(inb, size_remain, (Struct2*)(*o));

        break;
    default:
        return;
    }
}
uint32_t lmcp_pack(uint8_t* buf, lmcp_object* o) {
    uint8_t* outb = buf;
    switch (o->type) {
    case 1:
        outb += lmcp_pack_Struct1_header(outb, (Struct1*)o);
        outb += lmcp_pack_Struct1(outb, (Struct1*)o);
        return (outb - buf);

        break;
    case 2:
        outb += lmcp_pack_Struct2_header(outb, (Struct2*)o);
        outb += lmcp_pack_Struct2(outb, (Struct2*)o);
        return (outb - buf);

        break;
    default:
        return 0;
    }
}
