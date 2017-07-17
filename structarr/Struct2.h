
#pragma once
#include <stdlib.h>
#include <inttypes.h>
#include <string.h>
#include "common/struct_defines.h"
#include "common/conv.h"
#include "Struct1.h"
#define LMCP_Struct2_SUB "mytst.tst.Struct2"

#define LMCP_Struct2_TYPENAME "Struct2"

typedef struct {
    lmcp_object super;
    Struct1** field2;
    array_info field2_ai;

} Struct2;
size_t lmcp_packsize_Struct2 (Struct2* i);
size_t lmcp_pack_Struct2_header(uint8_t* buf, Struct2* i);
void lmcp_free_Struct2(Struct2* i);
void lmcp_init_Struct2 (Struct2** i);
void lmcp_unpack_Struct2(uint8_t** buf, size_t *size_remain,Struct2* outp);
size_t lmcp_pack_Struct2(uint8_t* buf, Struct2* i);
