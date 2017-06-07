
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
    uint32_t field1;

} Struct1;
uint32_t lmcp_packsize_Struct1 (Struct1* i);
size_t lmcp_unpack_Struct1(uint8_t* buf, Struct1** outp);
void lmcp_init_Struct1 (Struct1** i);
void lmcp_free_Struct1(Struct1* i);
size_t lmcp_pack_Struct1(uint8_t* buf, Struct1* i);
