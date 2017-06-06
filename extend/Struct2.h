
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
Struct1* super;
uint32_t field2;

}Struct2;uint32_t lmcp_packsize_Struct2 (Struct2* i);
size_t lmcp_unpack_Struct2(uint8_t* buf, Struct2** outp);
void lmcp_init_Struct2 (Struct2* i);
size_t lmcp_pack_Struct2(uint8_t* buf, Struct2* i);