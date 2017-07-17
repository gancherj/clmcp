
#pragma once
#include <stdlib.h>
#include <inttypes.h>
#include <string.h>
#include "common/struct_defines.h"
#include "common/conv.h"
#define LMCP_Struct1_SUB "mytst.tst.Struct1"

#define LMCP_Struct1_TYPENAME "Struct1"

typedef struct {
    lmcp_object super;
    uint16_t field1;

} Struct1;
size_t lmcp_packsize_Struct1 (Struct1* i);
size_t lmcp_pack_Struct1_header(uint8_t* buf, Struct1* i);
void lmcp_free_Struct1(Struct1* i);
void lmcp_init_Struct1 (Struct1** i);
void lmcp_unpack_Struct1(uint8_t** buf, size_t *size_remain,Struct1* outp);
size_t lmcp_pack_Struct1(uint8_t* buf, Struct1* i);
